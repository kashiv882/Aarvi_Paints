from rest_framework . views import APIView
from rest_framework . response import Response
from rest_framework import status
from .models import Gallery
from .serializers import Galleryserializers, PaintBudgetCalculatorSerializer


class GalleryView (APIView):
    def get(self , request):
        object_type = request.query_params.get('object_type')

        valid_choices = dict(Gallery.OBJECT_TYPE_CHOICES)
        if object_type not in valid_choices:
            return Response({'error': 'Invalid object_type provided.'}, status=status.HTTP_400_BAD_REQUEST)

        galleries = Gallery.objects.filter(object_type = object_type)

        if not galleries.exist():
            return Response({"error": "No galleries found for the provided object_type."},status=status.HTTP_404_NOT_FOUND)

        serializer = Galleryserializers(galleries, many=True)
        return Response(serializer.data)


class PaintBudgetCalculatorView(APIView):
    def post(self, request):
       try :

           user_info_data = request.data.get("user_info")

           if not user_info_data:
               return Response({"error": "user_info is required."}, status=status.HTTP_400_BAD_REQUEST)

           if user_info_data.get("object_type") != "userinfo":
               return Response({"error": "Invalid object_type. Must be 'userinfo'."}, status=status.HTTP_400_BAD_REQUEST)

           metadata = user_info_data.get("metadata")
           if not isinstance(metadata, dict):
               return Response({"error": "metadata must be a valid JSON object."}, status=status.HTTP_400_BAD_REQUEST)

           required_fields = ["area_type", "surface_condition", "selected_product", "entered_area"]
           for field in required_fields:
               if field not in request.data:
                   return Response({"error": f"{field} is required."}, status=status.HTTP_400_BAD_REQUEST)

           gallery = Gallery.objects.create(
               object_type="userinfo",
               metadata=metadata,
           )

           paint_data = {
                "area_type": request.data["area_type"],
                "surface_condition": request.data["surface_condition"],
                "selected_product": request.data["selected_product"],
                "entered_area": request.data["entered_area"],
                "gallery": str(gallery.id)
           }
           serializer = PaintBudgetCalculatorSerializer(data=paint_data)
           serializer.is_valid(raise_exception=True)
           serializer.save()

           return Response({
               "message": "Paint budget and user info saved successfully.",
               "data": serializer.data
           }, status=status.HTTP_201_CREATED)

       except Exception as e:
                return Response({
                    "message": "An unexpected error occurred.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

