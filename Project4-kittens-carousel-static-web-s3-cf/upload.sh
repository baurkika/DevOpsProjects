aws s3 ls # should list all the buckets
aws s3 ls | grep kittens # should list buckets containing "kittens" keyword
aws s3 ls s3://kittens.clarusway.us #should return empty
aws s3 sync ./static-web s3://kittens.clarusway.us
aws s3 ls s3://kittens.clarusway.us #should see list of website content