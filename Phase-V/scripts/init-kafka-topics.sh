#!/bin/bash
# T-V-05: Initialize Kafka Topics in Redpanda
# From: speckit.plan - Event-Driven Architecture

set -e

echo "Waiting for Redpanda to be ready..."
sleep 10

# Create topics using rpk (Redpanda CLI)
docker exec redpanda rpk topic create task-events \
    --partitions 3 \
    --replicas 1 \
    --config retention.ms=604800000 \
    --config cleanup.policy=delete

docker exec redpanda rpk topic create reminders \
    --partitions 3 \
    --replicas 1 \
    --config retention.ms=86400000 \
    --config cleanup.policy=delete

docker exec redpanda rpk topic create task-updates \
    --partitions 3 \
    --replicas 1 \
    --config retention.ms=3600000 \
    --config cleanup.policy=delete

echo "Topics created successfully:"
docker exec redpanda rpk topic list

echo ""
echo "Topic configurations:"
docker exec redpanda rpk topic describe task-events
docker exec redpanda rpk topic describe reminders
docker exec redpanda rpk topic describe task-updates
