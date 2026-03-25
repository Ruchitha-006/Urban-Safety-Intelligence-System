from django.http import JsonResponse
import pandas as pd
import os

def get_crimes(request):
    file_path = os.path.join('data', 'crime_data.csv')

    if not os.path.exists(file_path):
        return JsonResponse({"error": "CSV not found"}, status=404)

    df = pd.read_csv(file_path)
    data = df.to_dict(orient='records')

    return JsonResponse(data, safe=False)