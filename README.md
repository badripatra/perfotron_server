# Dynamic-LoadTest(Load & Performance Testing Platform)

The Tool offers setting up live performance monitoring environment for load testing suite built on jmeter.
 
It also facilitate setting up Jenkins to run Jmeter Tests.

## About

```            
            Target Audience      : Any individual / group using Jmeter for Performance Testing            
            How it helps         : Setting up Performance Testing environment End to End                                   
            Visualization        : Grafana (6.0.1)            
            Datasource           : Influx (1.7.4)            
            Load Test Tool       : Apache Jmeter (5.1.1)            
            Programming Language : Python 2.7, Shell Scripting            
            Hosting Servers      : i.  Grafana and Influx for Hosting Performance Dashboard
                                   ii. Jenkins for initiating Load Test                                   
            Supported Envs       : Unix (Ubuntu,CentOS, RHEL) for Hosting Server                                   
            System Configuration : Minimum 8 GB RAM for Hosting Server            
            Tested with          : 2 Thread Group - 1000 threads each                        
            Approx. Set Up Time  : 10 -15 Minutes
```

## Sequence of steps performed for setting up the environment

``` 
1. Enabling Required Ports ( 3000 for Grafana, 8086 & 8088 for Influx, 9003 for demo api, 8080 for jenkins)
2. Installing influx
3. Installing and setting up Grafana Server (Including setting up default data source and dashboard)
4. Setting up demo_jmeter script
5. Deploying a sample api for load testing
6. Deploying stats collector collecting and plotting vital stats like cpu, memory, disk usage of the Grafana Server
7. Setting up Jenkins - If opted
8. Triggering a demo run from Jenkins
9. If not opted for Jenkins  then  triggering a standalone run from your system
```


## Express set up

Pre-requsite :

```bash
1. git
2. Python 2.7
```

Technology/Tools used:

```bash
1. Grafana
2. Influx
3. Jmeter
4. Jenkins
```

How to run  the Tool and set up performance dashboard for Live Monitoring :

```bash
Step 1. Clone the Repo : git clone https://badri_patra@bitbucket.org/badri_patra/perfotron.git
Step 2. To start the setup : python perfotron
Step 3. Select 'Yes' or 'No' to proceed after reading Tool Usage and Instllation details
Step 4. Select 'Yes' or 'No' for instllating jenkins for demo runs
Step 5. Check the Jenkins Run Details for Load Test run from Jenkins
Step 6. Check the Grafana URL for Live Monitoring of Load Test
Step 7. Check Env Details from env_details.yaml
Step 8. To convert your jmx to run in this env, use the command "python perfotron --jmx sample_user_testplan.jmx"
Step 9. To uninstall the Tool, use command "python perfotron --uninstall"
```