import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_url = "https://10.0.15.183/restconf"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
} # Add
basicauth = ("admin", "cisco")

# check interface
def get():
    resp = requests.get(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070157", #
        auth=basicauth,
        headers=headers,
        verify=False
        )
    
    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        return bool(json.dumps(response_json, indent=4))
    
# create
def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070157",
            "description": "created loopback by RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.157.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    } # Add

    check = get()
    if check == True:
        return "Cannot create: Interface loopback 65070157"
    else:
        resp = requests.put(
            api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070157", # Add
            data=json.dumps(yangConfig), # Add
            auth=basicauth, 
            headers=headers, # Add 
            verify=False
            )

        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface Loopback65070157 created."
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Cannot create: Interface loopback 65070157" # Add

#delete
def delete():
    resp = requests.delete(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070157", # Add
        auth=basicauth, 
        headers=headers, # Add
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070157 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 65070157" # Add

# enable
def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070157",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
        } # Add
    }

    resp = requests.patch(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070157", # Add
        data=json.dumps(yangConfig), # Add
        auth=basicauth, 
        headers=headers, # Add
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070157 is enabled successfully" # Add
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 65070157" # Add
        
#disable
def disable():
    yangConfig = yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070157",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
        } # Add
    }

    resp = requests.patch(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070157", # Add
        data=json.dumps(yangConfig), # Add
        auth=basicauth, 
        headers=headers, # Add
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070157 is shutdowned successfully" # Add
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback 65070157" # Add
#status   
def status():
    resp = requests.get(
            api_url + "/data/ietf-interfaces:interfaces-state/interface=Loopback65070157",
            auth=basicauth, 
            headers=headers, # Add
            verify=False
        )
    
    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        print(json.dumps(response_json, indent=4))
        interface_name = response_json["ietf-interfaces:interface"]["name"]
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if(admin_status == 'up' and oper_status == 'up' and interface_name == 'Loopback65070157'):
            return "Interface loopback 65070157 is enabled"
        elif(admin_status == 'down' and oper_status == 'down' and interface_name == 'Loopback65070157'):
            return "Interface loopback 65070157 is disabled"
        elif(interface_name != 'Loopback65070157'):
            return "No Interface loopback 65070157"
        
    else:
        return "No Interface loopback 65070157"
    
def gigabit_status():
    resp = requests.get(
        f"{api_url}/data/ietf-interfaces:interfaces/interface=GigabitEthernet1",
        auth=basicauth,
        headers=headers,
        verify=False
    )
    
    if resp.status_code == 200:
        interface_data = resp.json()
        return f"GigabitEthernet1 status: {interface_data}"
    else:
        print(f'Error. Status Code: {resp.status_code}')
        return "Cannot retrieve GigabitEthernet1 status."

def showrun():
    resp = requests.get(
        f"{api_url}/data/Cisco-IOS-XE-native:native",  # ระบุ path ของ show run
        auth=basicauth,
        headers=headers,
        verify=False
    )
    
    if resp.status_code == 200:
        return resp.text  # ส่งคืนข้อมูลที่ได้จาก API
    else:
        print(f'Error. Status Code: {resp.status_code}')
        return None  # ถ้าไม่ได้ข้อมูลให้ส่งค่า None กลับไป