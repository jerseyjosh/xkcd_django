from django.core.management.base import BaseCommand
from comics.models import Comic
from fetch_xkcd_data.tasks import generate_embedding
import numpy as np
import asyncio


class Command(BaseCommand):
    help = "Search comics based on semantic similarity using OpenAI embeddings."

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Search query')

    def handle(self, *args, **options):
        # get query from arguments
        query = options['query']
        self.stdout.write(f"Searching for: {query}")

        # generate embedding
        query_embedding = asyncio.run(generate_embedding(query))

        if not query_embedding:
            self.stdout.write(self.style.ERROR("Failed to generate embedding for query."))
            return

        # fetch comics with embeddings
        comics = Comic.objects.exclude(embedding=None)

        # cosine similarity
        def cosine_similarity(vec1, vec2):
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        # similarity scores
        results = []
        for comic in comics:
            similarity = cosine_similarity(query_embedding, comic.embedding)
            results.append((similarity, comic))

        # get most similar
        results.sort(reverse=True, key=lambda x: x[0])
        top_results: list[tuple[list, Comic]] = results[:3]

        # output
        self.stdout.write(self.style.SUCCESS("\nTop Results:\n"))
        for similarity, comic in top_results:
            self.stdout.write(f"#{comic.comic_number}: {comic.title}")
            self.stdout.write(f"{comic.transcript}")
            self.stdout.write(f"{comic.image_url}")
            self.stdout.write(f"  Similarity: {similarity:.4f}")
            self.stdout.write("------")

        # self.stdout.write(self.style.SUCCESS("\nBottom Results:\n"))
        # for similarity, comic in results[-3:]:
        #     self.stdout.write(f"#{comic.comic_number}: {comic.title} - {comic.transcript}")
        #     self.stdout.write(f"  Similarity: {similarity:.4f}")
        #     self.stdout.write("------")
