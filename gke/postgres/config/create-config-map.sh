#!/bin/sh
kubectl create configmap postgres --from-file=postgres.conf --from-file=master.conf --from-file=pg_hba.conf
