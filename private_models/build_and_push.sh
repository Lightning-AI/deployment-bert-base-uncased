aws ecr get-login-password --region $LIGHTNING_CLUSTER_PRIMARY_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$LIGHTNING_CLUSTER_PRIMARY_REGION.amazonaws.com
aws ecr create-repository --repository-name litserve-bert-base-uncased --region $LIGHTNING_CLUSTER_PRIMARY_REGION || true
docker build -t $AWS_ACCOUNT_ID.dkr.ecr.$LIGHTNING_CLUSTER_PRIMARY_REGION.amazonaws.com/litserve-bert-base-uncased:latest .
docker push $AWS_ACCOUNT_ID.dkr.ecr.$LIGHTNING_CLUSTER_PRIMARY_REGION.amazonaws.com/litserve-bert-base-uncased:latest
echo $AWS_ACCOUNT_ID.dkr.ecr.$LIGHTNING_CLUSTER_PRIMARY_REGION.amazonaws.com/litserve-bert-base-uncased:latest