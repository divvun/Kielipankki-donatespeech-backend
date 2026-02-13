# Vake CDK deployment

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template

## How to create a environment from scratch

### Parameters and secrets to store to the accounts

#### Parameter store SSM keys

| Key | Value |
|-----|-------|
| /yle/client/id | Yle application id as plain text |
| /yle/client/key | Yle application key as plain text |
| /yle/decrypt | Yle decrypt key USE SecureString |

#### SecretsManager

| Key | Value |
|-----|-------|
| /github/oauthtoken |  { "oAuthToken" : [TOKEN] } |

#### Create hosted zones manually and provision CI pipeline using cdk

Create the needed hosted zone e.g. lahjoitapuhetta.fi and direct to domain to that DNS server.

When the needed parameters and secrets are set go to the cdk folder and run

```bash
npm run build
export ENV=prod
export BRANCH=master
cdk deploy VakeBackendCI --profile [AWS-PROFILE-FOR_TARGET_ACCOUNT]
```

When the deployment is done WAF needs to be attached to the cloudfront distribution manually ATM. So do this now.

After the production account is created create the hostedzone for the dev environment and then create the NS record 
to production to point to the dev env hosted zone.

```bash
export ENV=dev
export BRANCH=dev
cdk deploy VakeBackendCI --profile [AWS-PROFILE-FOR_TARGET_ACCOUNT]
```

And voila you should be done!
