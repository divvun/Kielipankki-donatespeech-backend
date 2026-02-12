import * as cdk from 'aws-cdk-lib';
import * as waf2 from 'aws-cdk-lib/aws-wafv2';
import { Construct } from 'constructs';

export class RecorderWAF extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vendorIPs = new waf2.CfnIPSet(this, "VendorIPs", {
        addresses: [
        ],
        ipAddressVersion: "IPV4",
        scope: 'CLOUDFRONT'
    })

    const waf = new waf2.CfnWebACL(this, "WebWAF", {
        name: "WebWAF",
        defaultAction: { block : {} },
        rules: [
            {
                name: "AllowVendorIPs",
                priority: 1,
                action: { allow: {}},
                statement: {
                    ipSetReferenceStatement: {
                        arn: vendorIPs.attrArn
                    }
                },
                visibilityConfig: {
                    cloudWatchMetricsEnabled: false,
                    metricName: "WAF-Allowed",
                    sampledRequestsEnabled: false,
                }
            }
        ],
        scope: 'CLOUDFRONT',
        visibilityConfig: {
            cloudWatchMetricsEnabled: true,
            metricName: "WAF-Blocked",
            sampledRequestsEnabled: false,
        },
    })

    new cdk.CfnOutput(this, 'WafArnOut', { value: waf.attrArn });

  }
}