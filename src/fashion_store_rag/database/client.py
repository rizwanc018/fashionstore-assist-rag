import weaviate
from weaviate.classes.init import Auth

from fashion_store_rag.config.settings import (
    WEAVIATE_API_KEY,
    WEAVIATE_URL,
)


def get_weaviate_client():
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
        skip_init_checks=True,
    )


with get_weaviate_client() as client:
    print("Connected:", client.is_ready())
