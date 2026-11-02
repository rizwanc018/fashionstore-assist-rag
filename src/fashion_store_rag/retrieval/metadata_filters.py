from weaviate.classes.query import Filter

from fashion_store_rag.query_understanding.metadata_extractor import ProductMetadata


def build_metadata_filters(metadata: ProductMetadata):
    filters = []

    text_fields = ["category", "sub_category", "color", "gender", "season", "usage"]

    for field in text_fields:
        value = getattr(metadata, field)

        if value is not None:
            filters.append(Filter.by_property(field).equal(value))

    if metadata.fabric is not None:
        filters.append(Filter.by_property("fabric").like(f"*{metadata.fabric}*"))

    if metadata.sizes:
        filters.append(Filter.by_property("sizes").contains_any(metadata.sizes))

    if metadata.min_price is not None:
        filters.append(Filter.by_property("price").greater_or_equal(metadata.min_price))

    if metadata.max_price is not None:
        filters.append(Filter.by_property("price").less_or_equal(metadata.max_price))

    if not filters:
        return None

    combined_filter = filters[0]

    for curr_filter in filters[1:]:
        combined_filter = combined_filter & curr_filter

    return combined_filter
