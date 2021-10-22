import {Construct} from 'constructs';
import {Names} from 'cdk8s';
import {KubeDeployment, KubeService, IntOrString, EnvVar} from '../imports/k8s';

export interface ServiceProps {
    /**
     * The Docker image to use for this service.
     */
    readonly image: string;

    /**
     * Number of replicas.
     *
     * @default 1
     */
    readonly replicas?: number;

    readonly port: number;

    readonly protocol?: string;
    readonly protocolName?: string;

    readonly containerPort: number;

    readonly env: EnvVar[];

    readonly hostname: string;
}

export class Service extends Construct {

    constructor(scope: Construct, id: string, props: ServiceProps) {
        super(scope, id);

        const image = props.image;
        const port = props.port;
        const containerPort = props.containerPort;
        const label = {app: Names.toDnsLabel(this)};
        const replicas = props.replicas ?? 1;
        const hostname = props.hostname;

        if (!props.protocol || !props.protocolName) {
            new KubeService(this, 'service', {
                metadata: {name: hostname},
                spec: {
                    type: 'LoadBalancer',
                    ports: [{port: port, targetPort: IntOrString.fromNumber(containerPort)}],
                    selector: label
                }
            });
        } else {
            new KubeService(this, 'service', {
                metadata: {name: hostname},
                spec: {
                    type: 'LoadBalancer',
                    ports: [{
                        name: props.protocolName,
                        protocol:props.protocol,
                        port: port,
                        targetPort: IntOrString.fromNumber(containerPort)
                    }],
                    selector: label
                }
            });
        }

        new KubeDeployment(this, 'deployment', {
                spec: {
                    replicas,
                    selector: {
                        matchLabels: label
                    },
                    template: {
                        metadata: {labels: label},
                        spec: {
                            dnsConfig:{
                                nameservers: ["127.0.0.1"]
                            },
                            hostname: hostname,
                            subdomain: 'sub-domain',
                            containers: [
                                {
                                    name: String(hostname+"test2"),
                                    image: image,
                                    ports: [{containerPort}],
                                    env: props.env,
                                    resources:{
                                        limits:{
                                            memory: "0Mi",
                                            cpu: "0m"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        );
    }
}