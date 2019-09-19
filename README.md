Automate EC2 Snap restore operation
This Script will be used for automation AWS snap restore operation. This is created by suddhasil Sarkar(suddhasil.sarkar@accenture.com)
this script can be used in any AWS environment where TAG is well implemented for services like instance, EBS volumes and snapshots
 At a glance the functionality of this script as is follows..
 1. Script is written in python 3.7.4 , it is required boto3 module to be configured and connection with AWS account a must need
 1. Mention the instance id for which restoration needs to be initiated
 2. Mention the specific date in "YYYY-MM-DD HH"  format for which you want to restore the data. As an example i Want restore snap which was taken on
    27th August 2019 @09 AM , then I need to pass on "2019-08-27 09" as the input parameter value ( script use UTC as default timezone )
 3. Script will create volumes from the snaps which was created on the above given date and time. ALl volumes will have tag value taken from ec2 instance
 4. Existing volumes which are already attached with the servers will get detached and new volumes will be attached with same device notation, ie - xvda, xvdc, etc..
