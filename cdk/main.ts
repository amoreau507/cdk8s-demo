import {Construct} from 'constructs';
import {App, Chart, ChartProps} from 'cdk8s';
import {Service} from "./lib/service";

export class MyChart extends Chart {
    constructor(scope: Construct, id: string, props: ChartProps = {}) {
        super(scope, id, props);

        const rabbitmq_username:string = 'username';
        const rabbitmq_password:string = 'password';

        const dynamoDB_username:string = 'admin';
        const dynamoDB_password:string = 'admin';

        const rabbitmq_props = {
            image: 'rabbitmq:3-management-alpine',
            replicas: 1,
            port:5672,
            containerPort: 5672,
            hostname: 'rabbitmq',
            env: [
                {
                    name: 'RABBITMQ_DEFAULT_USER',
                    value: rabbitmq_username
                },
                {
                    name: 'RABBITMQ_DEFAULT_PASS',
                    value: rabbitmq_password
                }
            ]
        };
        const dynamoDB_props = {
            image: 'mongo:4.2',
            replicas: 1,
            port:27017,
            containerPort: 27017,
            hostname: 'db',
            env: [
                {
                    name: 'MONGO_INITDB_ROOT_USERNAME',
                    value: dynamoDB_username
                },
                {
                    name: 'MONGO_INITDB_ROOT_PASSWORD',
                    value: dynamoDB_password
                },
                {
                    name: 'MONGO_INITDB_DATABASE',
                    value: 'mongo'
                }
            ]
        };

        new Service(this, 'rabbitmq', rabbitmq_props);
        new Service(this, 'dynamoDB', dynamoDB_props);


        const serviceEnv = [
                {
                    name: 'DB_HOSTNAME',
                    value: dynamoDB_props.hostname
                },
                {
                    name: 'DB_USERNAME',
                    value: dynamoDB_username
                },
                {
                    name: 'DB_PASSWORD',
                    value: dynamoDB_password
                },
                {
                    name: 'DB_PORT',
                    value: String(dynamoDB_props.containerPort)
                },
                {
                    name: 'DB_NAME',
                    value: 'mongo'
                },
                {
                    name: 'RABBITMQ_DEFAULT_USER',
                    value: rabbitmq_username
                },
                {
                    name: 'RABBITMQ_DEFAULT_PASS',
                    value: rabbitmq_password
                },
                {
                    name: 'RABBITMQ_HOSTNAME',
                    value: rabbitmq_props.hostname
                },
                {
                    name: 'RABBITMQ_POST',
                    value: String(rabbitmq_props.containerPort)
                }
            ];

        new Service(this, 'endpoint', {
            image: 'public.ecr.aws/u5o6b5p7/cdk8demo:endpoint',
            replicas: 1,
            protocolName: 'http',
            protocol: 'TCP',
            port: 30157,
            containerPort: 5000,
            hostname: 'endpoint',
            env: serviceEnv
        });

        new Service(this, 'service', {
            image: 'public.ecr.aws/u5o6b5p7/cdk8demo:service',
            replicas: 1,
            port:4321,
            containerPort: 4321,
            hostname: 'service',
            env: serviceEnv
        });
    }
}

const app = new App();
new MyChart(app, 'cdk');
app.synth();
