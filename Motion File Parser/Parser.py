import ASF
import re


def process_asf_amc(asf_fname, amc_fname):
	asf_file = open(asf_fname, 'r')
	asf_contents = asf_file.read() # Read entire contents.
	sections = asf_contents.split(':')
	root = None
	segments = list()
	for section in sections:
		dat = re.split('\W+', section, 1)
		name = dat[0]
		if name == 'root':
			root = ASF.Root.parse_root(dat[1])
		elif name == 'bonedata':
			segments = ASF.Segment.parse_bone_data(dat[1])
		else:
			continue
	asf = ASF.ASF(root, segments)

if __name__ == '__main__':
	process_asf_amc('MoCap Data/09.asf', 'MoCap Data/09_01.amc')