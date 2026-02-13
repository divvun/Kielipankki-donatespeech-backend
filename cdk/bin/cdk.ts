#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { VakeCI } from '../lib/vake-ci';
import { VakeBackendResources } from '../lib/vake-backend-resources';
import { VakeWAF } from '../lib/vake-waf';
import { VakeStaticSite } from '../lib/vake-frontend-hosting';

const app = new cdk.App();

const env = process.env['ENV'] || 'dev'

let subdomain = ""

if(env === 'dev') subdomain = "dev"

const domain = "lahjoitapuhetta.fi"

new VakeCI(app, 'VakeBackendCI', { env: { 
    region: 'eu-west-1'
}});

const euRegion = { 
                    env: { 
                        region: 'eu-west-1',
                        account: process.env['CDK_DEFAULT_ACCOUNT']
                    }
                 }

const usRegion = { env: { 
                        region: 'us-east-1',
                        account: process.env['CDK_DEFAULT_ACCOUNT']
                  }}

new VakeBackendResources(app, 'VakeBackendResources', { 
        domainName : domain, 
        siteSubDomain : subdomain,
    }, euRegion);

new VakeWAF(app, 'VakeWAF', usRegion);

new VakeStaticSite(app, "VakeStaticSite", { 
        domainName : domain, 
        siteSubDomain : subdomain,
    }, euRegion)
