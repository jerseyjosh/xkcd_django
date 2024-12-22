from django.core.management.base import BaseCommand
from comics.models import Comic
from fetch_xkcd_data.tasks import generate_embeddings
import asyncio


class Command(BaseCommand):
    help = "Generate embeddings for comics missing them."

    def handle(self, *args, **options):
        # fetch comics with missing embeddings
        missing_embeddings = Comic.objects.filter(embedding__isnull=True)
        texts = [item.transcript for item in missing_embeddings]
        # Generate embeddings for multiple texts
        embeddings = asyncio.run(generate_embeddings(texts))
        for comic, embedding in zip(missing_embeddings, embeddings):

            if embedding:  # only save if embedding generation was successful
                comic.embedding = embedding  
                comic.save()  # Save each comic
                self.stdout.write(self.style.SUCCESS(f"Saved embedding for comic {comic.comic_number}"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to generate embedding for comic {comic.comic_number}"))
