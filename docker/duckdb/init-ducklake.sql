INSTALL ducklake;
INSTALL postgres;
INSTALL httpfs;

LOAD ducklake;
LOAD postgres;
LOAD httpfs;

CREATE SECRET minio_secret (
    TYPE s3,
    KEY_ID '${MINIO_ROOT_USER}',
    SECRET '${MINIO_ROOT_PASSWORD}',
    ENDPOINT 'minio:9000',
    URL_STYLE 'path',
    USE_SSL false
);

ATTACH 'ducklake:postgres:dbname=${POSTGRES_DB} user=${POSTGRES_USER} password=${POSTGRES_PASSWORD} host=postgres port=5432' AS ducklake (
    DATA_PATH 's3://${MINIO_BUCKET}/ducklake'
);
