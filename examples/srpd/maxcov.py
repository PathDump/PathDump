#
# This script implements the max coverage algorithm in the following paper:
# Ramana Rao Kompella, Jennifer Yates, Albert Greenberg, Alex C Snoeren,
# "Detection and localization of network black holes", IEEE INFOCOM 2007.
#
#
import ctrlapi as capi

class maxcov():
    def __init__ (self, thresh):
        self.thresh     = thresh
        self.signatures = []

    def update_signature (self, flow):
        self.signatures.append (flow)

    def identify_candidates (self, lt):
        maxlinks = []
        prev     = None
        maxdict  = {}

        for link, stats in lt.items():
            maxdict.update ({link:stats["count"]})

        for w in sorted (maxdict, key = maxdict.get, reverse = True):
            if prev == None:
                prev = maxdict[w]
                maxlinks.append (w)
                continue
            elif prev != maxdict[w]:
                break
            elif prev == maxdict[w]:
                maxlinks.append (w)
            prev = maxdict[w]

        return maxlinks

    def greedy (self):
        observations = {}
        hypothesis   = {}

        for ob in self.signatures:
            pair = ob['flowid']['sip'] + '-' + ob['flowid']['dip']
            if pair not in observations:
                observations.update ({pair:[]})
            observations[pair].append (ob['path'])

        while len (observations) > 0:
            linktable = {}
            for pair, paths in observations.items():
                for path in paths:
                    for link in path:
                        if link not in linktable:
                            linktable.update ({link:{'count':0,'pairs':[]}})
                        linktable[link]['count'] += 1
                        linktable[link]['pairs'].append (pair)

            linkSet = self.identify_candidates (linktable)

            for l in linkSet:
                for pair in set(linktable[l]["pairs"]):
                    if pair in observations:
                        del observations[pair]

            for l in linkSet:
                hypothesis.update ({l:linktable[l]["count"]})
                del linktable[l]

        # choose final candidates who might be responsible for faults and drops
        candidates = []
        min_coverage = (self.thresh * len(self.signatures)) / 100
        for l, count in hypothesis.items():
            if count >= min_coverage:
                candidates.append (l)

        return candidates

if __name__ == "__main__":
    algo = maxcov (10)

    while True:
        try:
            flow = capi.getPoorTCPFlow()
            algo.update_signature (flow)
            candidates = algo.greedy()

            # enumerate suspicious links/interfaces
            print '\nPrinting suspicious links/interfaces:'
            for c in candidates:
                print c
        except KeyboardInterrupt:
            exit (0)
