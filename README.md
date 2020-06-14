# PerfoTron(Load & Performance Testing Platform)

The Tool offers setting up live performance monitoring environment for load testing suite built on jmeter.
 
It also facilitate setting up Jenkins to run Jmeter Tests.

## About

```            
            Target Audience      : Any individual / group using Jmeter for Performance Testing            
            How it helps         : Setting up Performance Testing environment End to End                                   
            Visualization        : Grafana           
            Datasource           : Influx            
            Load Test Tool       : Apache Jmeter          
            Programming Language : Python 2.7, Shell Scripting            
            Hosting Servers      : Grafana and Influx for Hosting Performance Dashboard                                                                     
            Supported Envs       : Unix (Ubuntu,CentOS, RHEL) for Hosting Server                                   
            System Configuration : Minimum 8 GB RAM for Hosting Server            
            Tested with          : 2 Thread Group - 1000 threads each                        
            Approx. Set Up Time  : 10 -15 Minutes
```

## Sequence of steps performed for setting up the environment

``` 
1. Enabling Required Ports ( 3000 for Grafana, 8086 for Influx, 9003 for demo api)
2. Installing influx
3. Installing and setting up Grafana Server (Including setting up default data source and dashboard)
4. Setting up demo_jmeter script
5. Deploying a sample api for load testing
6. Deploying stats collector collecting and plotting vital stats like cpu, memory, disk usage of the Grafana Server
7. Trigger sample jmeter script
8. Display details like Dasbhboard URL, Jmeter Script Location on screen
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
```

How to run  the Tool and set up PerfoTron dashboard for Live Monitoring :

```bash
Step 1. Clone the Repo : git clone https://github.com/badripatra/perfotron.git
Step 2. To start the setup : python perfotron
Step 3. Select 'Yes' or 'No' to proceed after reading Tool Usage and Instllation details
Step 4. Check the Grafana URL for Live Monitoring of Load Test
Step 5. Check Env Details from env_details.yaml
```
How to use PerfoTron Platform :

```bash
Pre-rquisite. Perfotron Dashboard should be installed
Step 1. For users with Jmeter Knowledge , use 'PerfoTron JMX Convertor' - http://<perfoTron_server_Ip>:9003/convert_jmx
Step 2. For users with no Jmeter Knowledge , use 'PerfoTron JMX Generator' - http://<perfoTron_server_Ip>:9003/convert_csv

```

How to uninstall Perfotron Dashboard :

```bash
Pre-rquisite. Perfotron Dashboard should be installed
Step 1. To uninstall the Perfotron, use command "python perfotron --uninstall"

How this option internally works :
1. Uninstallation of  Influx
2. Uninstallation of  Grafana
3. Kill existing instances of Influx, Grafana
4. Removing Files and Folder related to Influx, Grafana 
```
