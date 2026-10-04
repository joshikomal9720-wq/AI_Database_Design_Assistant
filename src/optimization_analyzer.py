class OptimizationAnalyzer:
    """
    Analyzes database relationships and constraints
    and suggests basic indexes and optimization tips.
    """

    def __init__(self):
        self.index_suggestions = []
        self.optimization_tips = []

    # ---------------------------------------------------------
    # INDEX SUGGESTIONS
    # ---------------------------------------------------------

    def suggest_indexes(
        self,
        foreign_keys,
        many_to_many_tables
    ):
        """Suggest indexes for foreign-key and junction columns."""

        self.index_suggestions = []

        # ---------------------------------------------
        # Foreign-key indexes
        # ---------------------------------------------

        for foreign_key in foreign_keys:

            table = foreign_key["table"]
            column = foreign_key["column"]

            suggestion = {
                "table": table,
                "column": column,
                "reason": "Foreign-key column"
            }

            if suggestion not in self.index_suggestions:

                self.index_suggestions.append(
                    suggestion
                )

        # ---------------------------------------------
        # Many-to-many junction-table indexes
        # ---------------------------------------------

        for junction in many_to_many_tables:

            table = junction["table"]

            entity1 = junction["entity1"]
            entity2 = junction["entity2"]

            entity1_column = (
                entity1.rstrip("s") + "_id"
            )

            entity2_column = (
                entity2.rstrip("s") + "_id"
            )

            suggestions = [
                {
                    "table": table,
                    "column": entity1_column,
                    "reason": "Many-to-Many relationship column"
                },
                {
                    "table": table,
                    "column": entity2_column,
                    "reason": "Many-to-Many relationship column"
                }
            ]

            for suggestion in suggestions:

                if suggestion not in self.index_suggestions:

                    self.index_suggestions.append(
                        suggestion
                    )

        return self.index_suggestions

    # ---------------------------------------------------------
    # OPTIMIZATION TIPS
    # ---------------------------------------------------------

    def generate_optimization_tips(
        self,
        foreign_keys,
        many_to_many_tables
    ):
        """Generate basic database optimization recommendations."""

        self.optimization_tips = []

        if foreign_keys:

            self.optimization_tips.append(
                "Foreign-key columns can benefit from indexing "
                "for faster joins and relationship lookups."
            )

        if many_to_many_tables:

            self.optimization_tips.append(
                "Junction-table relationship columns should "
                "be indexed for efficient Many-to-Many queries."
            )

            self.optimization_tips.append(
                "Composite UNIQUE constraints on junction tables "
                "help prevent duplicate relationships."
            )

        self.optimization_tips.append(
            "Avoid unnecessary indexes because indexes require "
            "additional storage and can slow INSERT and UPDATE operations."
        )

        self.optimization_tips.append(
            "Use appropriate data types to reduce storage usage "
            "and improve database efficiency."
        )

        self.optimization_tips.append(
            "Primary keys are automatically indexed by SQLite."
        )

        return self.optimization_tips

    # ---------------------------------------------------------
    # COMPLETE ANALYSIS
    # ---------------------------------------------------------

    def analyze(
        self,
        foreign_keys,
        many_to_many_tables
    ):
        """Perform complete database optimization analysis."""

        indexes = self.suggest_indexes(
            foreign_keys,
            many_to_many_tables
        )

        tips = self.generate_optimization_tips(
            foreign_keys,
            many_to_many_tables
        )

        return {
            "indexes": indexes,
            "tips": tips
        }

    # ---------------------------------------------------------
    # DISPLAY RESULTS
    # ---------------------------------------------------------

    def display_results(self, analysis):
        """Display optimization analysis results."""

        print("\n" + "=" * 70)
        print("DATABASE OPTIMIZATION ANALYSIS")
        print("=" * 70)

        print("\nSUGGESTED INDEXES")
        print("-" * 70)

        if analysis["indexes"]:

            for index in analysis["indexes"]:

                print(
                    f"✓ Index recommended for "
                    f"{index['table']}."
                    f"{index['column']}"
                )

                print(
                    f"  Reason: {index['reason']}"
                )

        else:

            print(
                "- No additional indexes suggested."
            )

        print("\nOPTIMIZATION TIPS")
        print("-" * 70)

        for tip in analysis["tips"]:

            print(
                f"✓ {tip}"
            )


# =============================================================
# TEST OPTIMIZATION ANALYZER
# =============================================================

if __name__ == "__main__":

    foreign_keys = [
        {
            "table": "orders",
            "column": "customer_id",
            "references": "customers(id)"
        },
        {
            "table": "payments",
            "column": "order_id",
            "references": "orders(id)"
        },
        {
            "table": "products",
            "column": "category_id",
            "references": "categories(id)"
        }
    ]

    many_to_many_tables = [
        {
            "table": "order_items",
            "entity1": "orders",
            "entity2": "products"
        }
    ]

    analyzer = OptimizationAnalyzer()

    analysis = analyzer.analyze(
        foreign_keys,
        many_to_many_tables
    )

    analyzer.display_results(
        analysis
    )