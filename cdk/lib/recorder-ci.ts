import * as cdk from "aws-cdk-lib";
import * as iam from "aws-cdk-lib/aws-iam";
import * as codebuild from "aws-cdk-lib/aws-codebuild";
import * as codepipeline from "aws-cdk-lib/aws-codepipeline";
import * as codepipelineActions from "aws-cdk-lib/aws-codepipeline-actions";
import { Duration } from "aws-cdk-lib";
import { BuildSpec, LinuxBuildImage } from "aws-cdk-lib/aws-codebuild";
import { Construct } from "constructs";

export class RecorderCI extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const env = process.env["ENV"] || "dev";
    const branch = process.env["BRANCH"] || "master";

    const githubArtifact = new codepipeline.Artifact("GithubArtifact");
    const serverlessArtifact = new codepipeline.Artifact("ServerlessArtifact");

    const pipeline = new codepipeline.Pipeline(
      this,
      "Recorder backend and frontend",
    );

    const oauth = cdk.SecretValue.secretsManager("/github/oauthtoken", {
      jsonField: "oAuthToken",
    });

    const githubAction = new codepipelineActions.GitHubSourceAction({
      actionName: "Source",
      output: githubArtifact,
      owner: "<github-user-name>",
      repo: "recorder-backend",
      branch: branch,
      oauthToken: oauth,
    });

    pipeline.addStage({
      stageName: "Source",
      actions: [githubAction],
    });

    const serverlessBuildRole = new iam.Role(this, "BuildRole", {
      assumedBy: new iam.ServicePrincipal("codebuild.amazonaws.com"),
    });

    serverlessBuildRole.addToPolicy(
      new iam.PolicyStatement({
        resources: ["*"],
        actions: [
          "s3:*",
          "iam:*",
          "kms:*",
          "logs:*",
          "acm:*",
          "cloudwatch:*",
          "codebuild:*",
          "cloudfront:*",
          "cloudformation:*",
          "apigateway:*",
          "lambda:*",
          "ssm:*",
          "ec2:*",
          "route53:*",
          "wafv2:*",
        ],
      }),
    );

    const serverlessBuild = new codebuild.PipelineProject(
      this,
      "Serverless build and deploy",
      {
        buildSpec: BuildSpec.fromSourceFilename("serverless_build_spec.yml"),
        environment: {
          buildImage: LinuxBuildImage.STANDARD_7_0,
          privileged: true,
          environmentVariables: {
            ENV: {
              type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
              value: env,
            },
            BRANCH: {
              type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
              value: branch,
            },
          },
        },
        role: serverlessBuildRole,
        timeout: Duration.minutes(60),
      },
    );

    pipeline.addStage({
      stageName: "BuildAndDeployServerless",
      actions: [
        new codepipelineActions.CodeBuildAction({
          actionName: "RunServerless",
          project: serverlessBuild,
          input: githubArtifact,
          outputs: [serverlessArtifact],
        }),
      ],
    });
  }
}
