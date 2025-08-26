#!/bin/bash
mongosh -- "$MONGO_INITDB_DATABASE" <<EOF
    var rootUser = '$MONGO_INITDB_ROOT_USERNAME';
    var rootPassword = '$MONGO_INITDB_ROOT_PASSWORD';
    var databaseName = "$MONGO_INITDB_DATABASE";
    var collectionName = 'users';

    var admin = db.getSiblingDB('admin');
    admin.auth(rootUser, rootPassword);

    var user = '$MONGO_INITDB_USERNAME';
    var passwd = '$MONGO_INITDB_PASSWORD';
    db.createUser({user: user, pwd: passwd, roles: [{ role: "readWrite", db: databaseName }]});

    db = db.getSiblingDB(databaseName);
    db.createCollection(collectionName);
    db[collectionName].drop();
EOF
