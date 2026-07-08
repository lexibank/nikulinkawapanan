import pathlib
from collections import defaultdict
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import FormSpec
from lingpy import Wordlist


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "nikulinkawapanan"
    form_spec = FormSpec(separators=";,~/", replacements=[(" ", "_")])

    writer_options = {'keep_languages': False, 'keep_parameters': False}

    def cmd_download(self, _):
        ...

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for concept in self.concepts:
            args.writer.add_concept(
                    ID=concept["ID"],
                    Name=concept["GLOSS"],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"]
                    )
            concepts[concept["GLOSS"]] = concept["ID"]
        args.log.info("added concepts")

        # add languages
        languages = {}
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"]
                    )
            languages[language["Name"]] = language["ID"]

        args.log.info("added languages")

        wl = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))
        c_set = defaultdict()
        counter = 1
        # add data
        for (
            _,
            number,
            entry,
            concept,
            doculect,
            value
        ) in pb(
            wl.iter_rows(
                "set",
                "entry",
                "concept",
                "doculect",
                "value"
            ),
            desc="cldfify"
        ):
            if value:
                # make sure that each row from the sheet is a cognate set
                if (number, entry) not in c_set:
                    c_set[(number, entry)] = counter
                    counter += 1

                args.writer.add_forms_from_value(
                    Language_ID=languages[doculect],
                    Parameter_ID=concepts[concept],
                    Value=value,
                    Cognacy=c_set[(number, entry)],
                    Source="Nikulin2022"
                    )
