from investiq.features.features import Feature


def bootstrap_feature_graph(roots: dict[str, Feature], features: list[Feature]) -> None:
    print("\nBootstrap running...\n")

    for feature in features:
        feature_name = feature.__dict__.get("name")

        if feature in roots.values():
            continue

        sources = feature.__dict__.get("_sources")
        print(f"Feature {feature_name} source {[s.__dict__.get("name") for s in sources]}")

        for s in sources:
            s.__dict__.get("_successors").append(feature)

    print("\nSuccessors : ")
    for f in features:
        print(f"Feature {f.name} successors {[s.__dict__.get("name") for s in f.successors]}")