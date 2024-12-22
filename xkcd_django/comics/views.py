from django.shortcuts import render
from .models import Comic
from fetch_xkcd_data.tasks import generate_embedding
import numpy as np
import asyncio

def comic_list(request):
    comics = Comic.objects.all().order_by('-comic_number')
    return render(request, 'comics/comic_list.html', {'comics': comics})

def search_comics(request):
    query = request.GET.get('q', '')  # Get search query
    results = []
    
    if query:
        # Generate the query embedding
        query_embedding = asyncio.run(generate_embedding(query))

        # Compute cosine similarity
        def cosine_similarity(vec1, vec2):
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        # Search through stored embeddings
        comics = Comic.objects.exclude(embedding=None)  # Only search comics with embeddings
        scores = []

        for comic in comics:
            similarity = cosine_similarity(query_embedding, comic.embedding)
            scores.append((similarity, comic))

        # Sort by similarity score (highest first)
        scores.sort(reverse=True, key=lambda x: x[0])
        results = [comic for _, comic in scores[:5]]  # Return top 5 results

    return render(request, 'comics/search_comics.html', {'query': query, 'results': results})
