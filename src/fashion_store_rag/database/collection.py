from weaviate.classes.config import Configure, DataType, Property

from fashion_store_rag.database.client import get_weaviate_client


def create_collections():
    with get_weaviate_client() as client:
        if not client.collections.exists("Products"):
            client.collections.create(
                name="Products",
                properties=[
                    Property(
                        name="product_id",
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    Property(
                        name="searchable_text",
                        data_type=DataType.TEXT,
                    ),
                    Property(
                        name="name",
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    Property(
                        name="category",
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    Property(
                        name="sub_category",
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    Property(
                        name="gender",
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    Property(
                        name="usage",
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    Property(
                        name="season",
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    Property(
                        name="color",
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    Property(
                        name="price",
                        data_type=DataType.NUMBER,
                        skip_vectorization=True,
                    ),
                ],
                vector_config=Configure.Vectors.text2vec_weaviate(
                    source_properties=["searchable_text"],
                ),
            )
            print("Products collection created.")

        # if not client.collections.exists("FAQs"):
        #     client.collections.create(
        #         name="FAQs",
        #         properties=[
        #             Property(
        #                 name="faq_id",
        #                 data_type=DataType.TEXT,
        #                 skip_vectorization=True,
        #             ),
        #             Property(
        #                 name="searchable_text",
        #                 data_type=DataType.TEXT,
        #             ),
        #             Property(
        #                 name="question",
        #                 data_type=DataType.TEXT,
        #                 skip_vectorization=True,
        #             ),
        #             Property(
        #                 name="answer",
        #                 data_type=DataType.TEXT,
        #                 skip_vectorization=True,
        #             ),
        #             Property(
        #                 name="category",
        #                 data_type=DataType.TEXT,
        #                 skip_vectorization=True,
        #             ),
        #         ],
        #         vector_config=Configure.Vectors.text2vec_weaviate(
        #             source_properties=["searchable_text"],
        #         ),
        #     )
        #     print("FAQs collection created.")


if __name__ == "__main__":
    create_collections()
