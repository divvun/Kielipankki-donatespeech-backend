import * as cdk from "aws-cdk-lib";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as acm from "aws-cdk-lib/aws-certificatemanager";
import * as route53 from "aws-cdk-lib/aws-route53";
import { Construct } from "constructs";
import { DomainProps, getSiteDomain } from "./common";

export class RecorderBackendResources extends cdk.Stack {
  constructor(
    scope: Construct,
    id: string,
    domainProps: DomainProps,
    props?: cdk.StackProps,
  ) {
    super(scope, id, props);

    const env = process.env["ENV"];
    const siteDomain = getSiteDomain(domainProps);

    // Content bucket
    const contentBucket = new s3.Bucket(this, "ContentBucket", {
      bucketName: "recorder-content-" + env,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      publicReadAccess: false,
      cors: [
        {
          allowedMethods: [s3.HttpMethods.PUT],
          allowedHeaders: ["Content-Type"],
          allowedOrigins: ["*"],
          maxAge: 600,
        },
      ],
    });

    const zone = route53.HostedZone.fromLookup(this, "HostedZone", {
      domainName: siteDomain,
    });

    // TLS certificate
    const certificateArn = new acm.DnsValidatedCertificate(
      this,
      "SiteCertificate",
      {
        domainName: "endpoint." + siteDomain,
        hostedZone: zone,
        region: "us-east-1",
      },
    ).certificateArn;

    new cdk.CfnOutput(this, "ContentBucketNameOut", {
      value: contentBucket.bucketName,
    });
    new cdk.CfnOutput(this, "ContentBucketArnOut", {
      value: contentBucket.bucketArn,
    });
    new cdk.CfnOutput(this, "EndpointCertificateArnOut", {
      value: certificateArn,
    });
    new cdk.CfnOutput(this, "HostedZoneIdOut", { value: zone.hostedZoneId });
    new cdk.CfnOutput(this, "SiteDomainOut", { value: siteDomain });
  }
}
