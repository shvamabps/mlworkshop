import boto3
import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=1)  # HandDetector session

cap = cv2.VideoCapture(0)  # cv2 video capture instance


INSTANCE_AMI = "ami-0a2acf24c0d86e927"  # aws instance ami
INSTANCE_TYPE = "t2.micro"  # aws instance type
INSTANCE_COUNT = 1  # aws instace count
RESOURCE_TYPE = "ec2"  # aws resource type
REGION = "ap-south-1"  # aws region
SECURITY_GROUP_ID = "sg-07c97700945cbdfa0"  # aws security group


ec2 = boto3.resource(RESOURCE_TYPE, REGION)  # EC2 resource session


allOs = []  # list of all launched instance ids


# Launch EC2 instance
def launchEC2Instance():
    instance = ec2.create_instances(  # create ec2 creation instance
        ImageId=INSTANCE_AMI,
        MinCount=INSTANCE_COUNT,
        MaxCount=INSTANCE_COUNT,
        InstanceType=INSTANCE_TYPE,
        SecurityGroupIds=[SECURITY_GROUP_ID],
    )
    instance_id = instance[0].id
    allOs.append(instance_id)
    print(f"Instance Id of started ec2 instance: {instance_id}", end="\n")
    print(f"Total number instances launched: {len(allOs)}", end="\n")
    return instance_id


# Remove EC2 instances
def removeEC2Instance():
    if len(allOs) > 0:
        osremove = allOs.pop()  # remove the last element from the list
        ec2.instances.filter(
            InstanceIds=[osremove]
        ).terminate()  # terminate ec2 instance
        print(f"Instance Id deleted: {osremove}", end="\n")
        print(f"Total number of instances left: {len(allOs)}", end="\n")
    else:
        print("No instances are currently running.")
    return


# Detect hand
def detectHand(image, draw=False):
    detector = HandDetector(maxHands=1)  # Hand Detector instance
    hand = detector.findHands(image, draw=draw)
    if hand:
        lmList = hand[0]
        totalFinger = detector.fingersUp(lmList)
        if totalFinger == [0, 1, 1, 0, 0]:  # 2 fingers detected (index, middle)
            print("Two fingers detected.", end="\n")
            launchEC2Instance()
        elif totalFinger == [0, 1, 0, 0, 0]:  # 1 finger detected (index)
            print("One fingers detected.", end="\n")
            removeEC2Instance()
        else:
            print("No fingers detected.", end="\n")
        return totalFinger
    print("No hand detected.")
    return


# live stream based detection
def liveDetector():
    while True:
        status, photo = cap.read()

        detectHand(photo)

        cv2.imshow("my photo", photo)

        if cv2.waitKey(1000) == 13:
            break
    cv2.destroyAllWindows()


# Only after the all the work is done, release cv2 camera instance
# cap.release()

# executing the detection function.
liveDetector()
