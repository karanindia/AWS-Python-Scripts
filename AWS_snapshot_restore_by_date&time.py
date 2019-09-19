'''
*********************************************************************************************************************************************************************
This Script will be used for automation AWS snap restore operation. This is created by suddhasil Sarkar(suddhasil.sarkar@accenture.com)
this script can be used in any AWS environment where TAG is well implemented for services like instance, EBS volumes and snapshots
 At a glance the functionality of this script as is follows..
 1. Script is written in python 3.7.4 , it is required boto3 module to be configured and connection with AWS account a must need
 1. Mention the instance id for which restoration needs to be initiated
 2. Mention the specific date in "YYYY-MM-DD HH"  format for which you want to restore the data. As an example i Want restore snap which was taken on
    27th August 2019 @09 AM , then I need to pass on "2019-08-27 09" as the input parameter value ( script use UTC as default timezone )
 3. Script will create volumes from the snaps which was created on the above given date and time. ALl volumes will have tag value taken from ec2 instance
 4. Existing volumes which are already attached with the servers will get detached and new volumes will be attached with same device notation, ie - xvda, xvdc, etc..
 *********************************************************************************************************************************************************************
'''

import boto3
import time

ec2 = boto3.client('ec2')
#volume_id = "something"
id = [input("Please Enter the instance id you want to restore:")]
#print(id)
ids = " ".join(str(x) for x in id)
# print(ids)
snapdate = input("please Enter the date you want to restore the data from in 'YYYY-MM-DD HH' format :")
volcount = 0
volcountstr = str(volcount)

# find the AZ in which the server is running , volumes must be created in same AZ
get_azs = ec2.describe_instances(Filters=[{'Name': 'instance-id', 'Values': id}])
# print(get_azs)
for response in get_azs['Reservations']:
    # print(response)
    for instance in response['Instances']:
        availability_zone = instance['Placement']['AvailabilityZone']
        # print(availability_zone)

# find instance tags which will be applied on restored EBS vols
get_tags = ec2.describe_instances(Filters=[{'Name': 'instance-id', 'Values': id}])
# print(get_tags)
for response in get_tags['Reservations']:
    # print(response)
    for instance in response['Instances']:
        tags = (instance['Tags'])
        # print(type(tags))


# finding snapshots created in specified date
def get_snapshots():
    response = ec2.describe_snapshots(
        Filters=[{'Name': 'tag:Name', 'Values': ['aws-test-1']}]
    )
    return response["Snapshots"]

# search for snapshots which matches the given Date Time
snapshots = [s for s in get_snapshots() if s["StartTime"].strftime('%Y-%m-%d %H') == snapdate]
#print(snapshots)
for snapshot in snapshots:
    # currentvol_ids = snapshot['VolumeId']
    # print(type(currentvol_ids))
    snap_ids = snapshot['SnapshotId']
    snaplist = [snap_ids]
    snapleng = (len(snaplist))
    #print(snapleng)
    volcount = volcount + snapleng
    snaps = [(snap_ids)]  # converting string into list

    for snap_id in snaps:  # creating volumes from the snaps
        print(snap_id + "....creating volume from :" + snap_id)
        vols = ec2.create_volume(AvailabilityZone=availability_zone, SnapshotId=snap_id,
                                 TagSpecifications=[{'ResourceType': 'volume', 'Tags': tags}])
        # print(vols) converting into list
        volumes = [vols]
        # print(type(volumes))
        for vol in volumes:
            vol_id = vol['VolumeId']
            print("\033[1;32m Created new volume:\033[1;m" + vol_id)
    time.sleep(10)

    for current_vol in [snapshot['VolumeId']]:
        temp = (ec2.describe_volumes(Filters=[{'Name': 'volume-id', 'Values': [current_vol]}])['Volumes'])
        # print(temp)
        for attachment in temp:
            attach_id = attachment['Attachments']
            for id in attach_id:
                volume_id = id['VolumeId']
                logical_id = id['Device']
                print("Current associated volume is :" + volume_id + "........" + logical_id)
                output = ec2.detach_volume(VolumeId=volume_id)
                # print(output)
                print("detaching volume...." + volume_id + "from instance:")
                print(logical_id)
                logicalid = (logical_id)
                time.sleep(10)
                attachvol = ec2.attach_volume(Device=logicalid, InstanceId=ids, VolumeId=vol_id)
                print("\033[1;32m Attaching new volume:\033[1;m" + vol_id + "\033[1;32m To the instance:\033[1;m"  + ids )

print("total " +((str(volcount))+"/"+ (str(volcount))) + " number of volumes created successfully")

