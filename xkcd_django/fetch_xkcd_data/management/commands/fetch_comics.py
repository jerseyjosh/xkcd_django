import asyncio
from django.core.management.base import BaseCommand
from fetch_xkcd_data.tasks import (
    fetch_all_comics, 
    fetch_latest_comic, 
    fetch_comics_range,
    format_date
)
from comics.models import Comic

class Command(BaseCommand):
    help = "Fetch XKCD comics asynchronously"

    def add_arguments(self, parser):
        parser.add_argument('--update', action='store_true', help='Update existing comics to most recent available')
        parser.add_argument('--latest', action='store_true', help='Fetch the latest comic')
        parser.add_argument('--range', nargs=2, type=int, help='Fetch a range of comics (start and end)')

    def handle(self, *args, **options):
        if options['update']:
            most_recent = Comic.objects.order_by('-comic_number').first()
            latest = asyncio.run(fetch_latest_comic())
            if most_recent.comic_number < latest['num']:
                comics = asyncio.run(fetch_comics_range(most_recent.comic_number + 1, latest['num']))
            else:
                self.stdout.write(self.style.SUCCESS("Comics are already up to date"))
                return
        if options['latest']:
            comics = [asyncio.run(fetch_latest_comic())]
        elif options['range']:
            start, end = options['range']
            comics = asyncio.run(fetch_comics_range(start, end))
        else:
            comics = asyncio.run(fetch_all_comics())
        self.save_comics(comics)

    def save_comics(self, comics: list[dict]):
        n_saved = 0
        for comic in comics:
            try:
                Comic.objects.update_or_create(
                    comic_number=comic['num'],
                    defaults={
                        'title': comic['title'],
                        'alt_text': comic['alt'],
                        'image_url': comic['img'],
                        'transcript': comic['transcript'],
                        'publish_date': format_date(comic),
                    }
                )
                n_saved += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error saving comic {comic['num']}: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Fetched and saved {n_saved} of {len(comics)} comics"))