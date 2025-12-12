from mrjob.job import MRJob
from mrjob.step import MRStep


class MRPageRank(MRJob):
    # Constants section
    DEFAULT_ITERATIONS = 10
    DEFAULT_DAMPING_FACTOR = 0.85    

    # Tags section
    TAG_GRAPH = 'GRAPH'
    TAG_RANK = 'RANK'


    def configure_args(self):
        super(MRPageRank, self).configure_args()
        self.add_passthru_arg(
            '--num-pages', type=int,
            help='Total number of pages (number of lines in the input file)'
        )
        self.add_passthru_arg(
            '--iterations', type=int, default=self.DEFAULT_ITERATIONS,
            help='Number of PageRank iterations'
        )
        self.add_passthru_arg(
            '--damping-factor', type=float, default=self.DEFAULT_DAMPING_FACTOR,
            help='Damping factor'
        )

    def mapper_first(self, _, line):
        # Format: page_id\toutlinks
        line = line.strip()
        if not line:
            return

        parts = line.split('\t')
        if not parts:
            return

        page_id = parts[0]
        outlinks = parts[1].split(',') if len(parts) > 1 and parts[1] else []

        initial_pagerank = 1.0 / self.options.num_pages

        yield page_id, (self.TAG_GRAPH, outlinks)

        if outlinks:
            contribution = initial_pagerank / len(outlinks)
            for outlink in outlinks:
                yield outlink, (self.TAG_RANK, contribution)

    def mapper_subsequent(self, page_id, value):
        # Format: page_id, "pagerank\toutlinks"
        parts = value.split('\t')
        current_pagerank = float(parts[0])
        outlinks = parts[1].split(',') if len(parts) > 1 and parts[1] else []

        yield page_id, (self.TAG_GRAPH, outlinks)

        if outlinks:
            contribution = current_pagerank / len(outlinks)
            for outlink in outlinks:
                yield outlink, (self.TAG_RANK, contribution)

    def reducer(self, page_id, values):
        outlinks = []
        total_rank = 0.0

        for value_type, data in values:
            if value_type == self.TAG_GRAPH:
                outlinks = data
            elif value_type == self.TAG_RANK:
                total_rank += data

        damping = self.options.damping_factor
        num_pages = self.options.num_pages
        new_pagerank = (1 - damping) / num_pages + damping * total_rank

        outlinks_str = ','.join(outlinks) if outlinks else ''
        yield page_id, f"{new_pagerank:.6f}\t{outlinks_str}"

    def steps(self):
        iterations = self.options.iterations
        steps = []

        steps.append(MRStep(
            mapper=self.mapper_first,
            reducer=self.reducer
        ))

        for _ in range(iterations - 1):
            steps.append(MRStep(
                mapper=self.mapper_subsequent,
                reducer=self.reducer
            ))

        return steps


if __name__ == '__main__':
    MRPageRank.run()
