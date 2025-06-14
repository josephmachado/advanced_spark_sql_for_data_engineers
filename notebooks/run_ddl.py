from pyspark.sql import SparkSession
from pathlib import Path
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger(__name__)

# Create Spark session
spark = SparkSession.builder.appName("Run DDLs for TPCH data").getOrCreate()

logger.info("Dropping any existing TPCH tables")
# Drop existing tables if they exist
spark.sql("DROP TABLE IF EXISTS prod.db.customer")
spark.sql("DROP TABLE IF EXISTS prod.db.lineitem")
spark.sql("DROP TABLE IF EXISTS prod.db.nation")
spark.sql("DROP TABLE IF EXISTS prod.db.orders")
spark.sql("DROP TABLE IF EXISTS prod.db.part")
spark.sql("DROP TABLE IF EXISTS prod.db.partsupp")
spark.sql("DROP TABLE IF EXISTS prod.db.region")
spark.sql("DROP TABLE IF EXISTS prod.db.supplier")


logger.info("Creating TPCH Iceberg tables")
# Create tables using Iceberg format
spark.sql("""
CREATE TABLE IF NOT EXISTS prod.db.customer (
  c_custkey    BIGINT,
  c_name       STRING,
  c_address    STRING,
  c_nationkey  BIGINT,
  c_phone      STRING,
  c_acctbal    DECIMAL(15,2),
  c_mktsegment STRING,
  c_comment    STRING
) USING iceberg
TBLPROPERTIES (
  'format-version' = '2'
)
""")

spark.sql("""
CREATE TABLE IF NOT EXISTS prod.db.lineitem (
  l_orderkey      BIGINT,
  l_partkey       BIGINT,
  l_suppkey       BIGINT,
  l_linenumber    INT,
  l_quantity      DECIMAL(15,2),
  l_extendedprice DECIMAL(15,2),
  l_discount      DECIMAL(15,2),
  l_tax           DECIMAL(15,2),
  l_returnflag    STRING,
  l_linestatus    STRING,
  l_shipdate      DATE,
  l_commitdate    DATE,
  l_receiptdate   DATE,
  l_shipinstruct  STRING,
  l_shipmode      STRING,
  l_comment       STRING
) USING iceberg
TBLPROPERTIES (
  'format-version' = '2'
)
""")

spark.sql("""
CREATE TABLE IF NOT EXISTS prod.db.nation (
  n_nationkey INT,
  n_name      STRING,
  n_regionkey INT,
  n_comment   STRING
) USING iceberg
TBLPROPERTIES (
  'format-version' = '2'
)
""")

spark.sql("""
CREATE TABLE IF NOT EXISTS prod.db.orders (
  o_orderkey      BIGINT,
  o_custkey       BIGINT,
  o_orderstatus   STRING,
  o_totalprice    DECIMAL(15,2),
  o_orderdate     DATE,
  o_orderpriority STRING,
  o_clerk         STRING,
  o_shippriority  INT,
  o_comment       STRING
) USING iceberg
TBLPROPERTIES (
  'format-version' = '2'
)
""")

spark.sql("""
CREATE TABLE IF NOT EXISTS prod.db.part (
  p_partkey     BIGINT,
  p_name        STRING,
  p_mfgr        STRING,
  p_brand       STRING,
  p_type        STRING,
  p_size        INT,
  p_container   STRING,
  p_retailprice DECIMAL(15,2),
  p_comment     STRING
) USING iceberg
TBLPROPERTIES (
  'format-version' = '2'
)
""")

spark.sql("""
CREATE TABLE IF NOT EXISTS prod.db.partsupp (
  ps_partkey    BIGINT,
  ps_suppkey    BIGINT,
  ps_availqty   INT,
  ps_supplycost DECIMAL(15,2),
  ps_comment    STRING
) USING iceberg
TBLPROPERTIES (
  'format-version' = '2'
)
""")

spark.sql("""
CREATE TABLE IF NOT EXISTS prod.db.region (
  r_regionkey INT,
  r_name      STRING,
  r_comment   STRING
) USING iceberg
TBLPROPERTIES (
  'format-version' = '2'
)
""")

spark.sql("""
CREATE TABLE IF NOT EXISTS prod.db.supplier (
  s_suppkey   BIGINT,
  s_name      STRING,
  s_address   STRING,
  s_nationkey BIGINT,
  s_phone     STRING,
  s_acctbal   DECIMAL(15,2),
  s_comment   STRING
) USING iceberg
TBLPROPERTIES (
  'format-version' = '2'
)
""")


def upsert_data(data_name, data_path=Path("/home/iceberg/notebooks/notebooks/data")):
    csv_path = data_path / f"{data_name}.csv"
    logger.info(f"Reading {data_name} data from {str(csv_path)}")
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("delimiter", ",")
        .option("inferSchema", "true")
        .load(str(csv_path))
    )
    df.writeTo(f"prod.db.{data_name}").overwritePartitions()


logger.info("Loading data into TPCH Iceberg tables")
upsert_data("customer")
upsert_data("lineitem")
upsert_data("nation")
upsert_data("orders")
upsert_data("part")
upsert_data("partsupp")
upsert_data("region")
upsert_data("supplier")
