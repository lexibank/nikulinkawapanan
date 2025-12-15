import pathlib
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from lingpy import Wordlist


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "nikulinkawapanan"

    writer_options = {'keep_languages': False, 'keep_parameters': False}

    def cmd_download(self, _):
        ...

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            concepts[concept.english] = idx

        args.log.info("added concepts")

        # add languages
        languages = {}
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"],
                    SubGroup=language["SubGroup"]
                    )
            languages[language["ID"]] = language["Name"]

        args.log.info("added languages")

        errors = set()
        # wl = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))
        # for item in wl:
        #   ...
