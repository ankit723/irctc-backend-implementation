from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .mongo import search_logs_collection


class TopRoutesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        pipeline = [
            {
                "$group": {
                    "_id": {
                        "source": "$source",
                        "destination": "$destination"
                    },
                    "search_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"search_count": -1}
            },
            {
                "$limit": 5
            }
        ]

        results = list(search_logs_collection.aggregate(pipeline))

        formatted = [
            {
                "source": r["_id"]["source"],
                "destination": r["_id"]["destination"],
                "search_count": r["search_count"]
            }
            for r in results
        ]

        return Response(formatted)