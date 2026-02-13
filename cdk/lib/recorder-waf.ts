import * as cdk from "@aws-cdk/core";
import waf2 = require("@aws-cdk/aws-wafv2");

export class RecorderWAF extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const solitaIPs = new waf2.CfnIPSet(this, "SolitaIPs", {
      addresses: [
        "109.204.231.126/32",
        "109.204.231.70/32",
        "109.204.231.81/32",
        "185.18.77.12/32",
        "194.157.227.124/32",
        "213.219.110.42/32",
        "85.194.237.84/32",
        "85.194.237.85/32",
        "87.108.77.102/32",
        "87.236.156.218/32",
        "89.41.48.226/32",
        "89.41.48.227/32",
        "89.41.48.228/32",
        "95.175.96.152/32",
      ],
      ipAddressVersion: "IPV4",
      scope: "CLOUDFRONT",
    });

    const waf = new waf2.CfnWebACL(this, "WebWAF", {
      name: "WebWAF",
      defaultAction: { block: {} },
      rules: [
        {
          name: "AllowSolitaIPs",
          priority: 1,
          action: { allow: {} },
          statement: {
            ipSetReferenceStatement: {
              arn: solitaIPs.attrArn,
            },
          },
          visibilityConfig: {
            cloudWatchMetricsEnabled: false,
            metricName: "WAF-Allowed",
            sampledRequestsEnabled: false,
          },
        },
      ],
      scope: "CLOUDFRONT",
      visibilityConfig: {
        cloudWatchMetricsEnabled: true,
        metricName: "WAF-Blocked",
        sampledRequestsEnabled: false,
      },
    });

    new cdk.CfnOutput(this, "WafArnOut", { value: waf.attrArn });
  }
}
