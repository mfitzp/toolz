# -------------------------------------------------------------------------
#     Copyright (C) 2008-2010 Martin Strohalm <mmass@biographics.cz>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE in the
#     main directory of the program
# -------------------------------------------------------------------------

# load libs
import xml.dom.minidom
from copy import deepcopy


# DEFAULT CONFIG VALUES
# ---------------------

version = '3.0.0'
build = 'alpha 1'
updates = 'http://mmass.biographics.cz/update.php'

main={
    'appWidth': 1000,
    'appHeight': 550,
    'appMaximized': 1,
    'mzDigits': 4,
    'intDigits': 0,
    'lastDir': '',
    'errorUnits': 'Da',
    'printQuality': 5,
    'macListCtrlGeneric': 1,
}

recent=[]

colours=[
    (16,71,185),
    (50,175,0),
    (241,144,0),
    (76,199,197),
    (143,143,21),
    (38,122,255),
    (38,143,73),
    (237,187,0),
    (120,109,255),
    (179,78,0),
    (128,191,189),
    (137,136,68),
    (200,136,18),
    (197,202,61),
    (123,182,255),
    (69,67,138),
    (24,129,131),
    (131,129,131),
    (69,126,198),
    (189,193,123),
    (127,34,0),
    (76,78,76),
    (31,74,145),
    (15,78,75),
    (79,26,81),
]

export={
    'imageWidth': 750,
    'imageHeight': 500,
    'imageUnits': 'px',
    'imageResolution': 72,
    'imageFormat': 'PNG',
    'peaklistColumns': ['mz','int'],
    'peaklistFormat': 'ASCII',
    'peaklistSeparator': 'tab',
    'spectrumSeparator': 'tab',
}

spectrum={
    'showGrid': 1,
    'showLegend': 1,
    'showPosBar': 1,
    'showGel': 1,
    'showGelLegend': 0,
    'showTracker': 1,
    'showLabels': 1,
    'showAllLabels': 1,
    'showTicks': 1,
    'posBarHeight': 10,
    'gelHeight': 19,
    'autoscale': 1,
    'overlapLabels': 0,
    'checkLimits': 1,
    'mzDigits': 4,
    'intDigits': 1,
    'labelAngle': 90,
    'labelCharge': 1,
    'labelBgr': 1,
    'labelFontSize': 10,
    'axisFontSize': 10,
    'tickColour': (255,100,100),
    'tmpSpectrumColour': (255,0,0),
    'matchPointsColour': (0,255,0),
}

match={
    'tolerance': 0.2,
    'units': 'Da',
    'ignoreCharge': 0,
}

processing={
    'crop':{
        'lowMass': 500,
        'highMass': 5000,
    },
    'smoothing':{
        'method': 'SG',
        'windowSize': 0.3,
        'cycles': 2,
    },
    'baseline':{
        'segments': 10,
        'offset': 0,
        'smooth': 1,
    },
    'peakpicking':{
        'peakWidth': 0.25,
        'snTreshold': 3,
        'absIntTreshold': 0,
        'relIntTreshold': 0,
        'smoothing': 0,
        'pickingHeight': 0.75,
        'adaptiveNoise': 0,
        'deisotoping': 1,
    },
    'deisotoping':{
        'maxCharge': 1,
        'massTolerance': 0.1,
        'intTolerance': 0.5,
        'removeIsotopes': 1,
        'removeUnknown': 1,
    },
}

calibration={
    'fitting': 'quadratic',
    'tolerance': 50,
    'units': 'ppm',
    'statCutOff': 800,
}

sequence={
    'digest':{
        'maxMods': 1,
        'maxCharge': 1,
        'massType': 0,
        'enzyme': 'Trypsin',
        'miscl': 1,
        'lowMass': 500,
        'highMass': 5000,
        'allowMods': 0,
        'listFormat': 'b.S.a [m]',
        'matchFormat': '[r] b.S.a [m]',
    },
    'fragment':{
        'maxMods': 1,
        'maxCharge': 1,
        'massType': 1,
        'fragments': ['a','b','y','-NH3','-H2O'],
        'filterFragments': 1,
        'listFormat': 'b.S.a [m]',
        'matchFormat': '[f] b.S.a [m]',
    },
    'search':{
        'mass': 0,
        'maxMods': 1,
        'maxCharge': 1,
        'massType': 0,
        'enzyme': 'Trypsin',
        'tolerance': 0.2,
        'units': 'Da',
        'listFormat': 'b.S.a [m]',
    },
}

masscalc={
    'ionseriesAgent': 'H',
    'ionseriesAgentCharge': 1,
    'ionseriesPolarity': 1,
    'patternFwhm': 0.1,
    'patternIntensity': 100,
    'patternBaseline': 0,
    'patternShift': 0,
    'patternTreshold': 0.001,
}

differences={
    'aminoacids': 1,
    'dipeptides': 1,
    'massType': 0,
    'tolerance': 0.1,
}

mascot={
    'servers':{
        'Matrix Science':{
            'host': 'www.matrixscience.com',
            'path': '/',
            'search': 'cgi/nph-mascot.exe',
            'results': 'cgi/master_results.pl',
            'export': 'cgi/export_dat_2.pl',
            'params': 'cgi/get_params.pl',
        },
    },
    'common':{
        'searchTitle':'',
        'userName':'',
        'userEmail':'',
        'server': 'Matrix Science',
        'searchType': 'pmf',
    },
    'pmf':{
        'database': 'SwissProt',
        'taxonomy': 'All entries',
        'enzyme': 'Trypsin',
        'miscleavages': 1,
        'fixedMods': [],
        'variableMods': [],
        'proteinMass': '',
        'peptideTol': 0.2,
        'peptideTolUnits': 'Da',
        'massType': 'Monoisotopic',
        'charge': '1+',
        'decoy': 0,
        'report': 'AUTO',
    },
    'sq':{
        'database': 'SwissProt',
        'taxonomy': 'All entries',
        'enzyme': 'Trypsin',
        'miscleavages': 1,
        'fixedMods': [],
        'variableMods': [],
        'peptideTol': 1.0,
        'peptideTolUnits': 'Da',
        'msmsTol': 0.5,
        'msmsTolUnits': 'Da',
        'massType': 'Average',
        'charge': '1+',
        'instrument': 'Default',
        'quantitation': 'None',
        'decoy': 0,
        'report': 'AUTO',
    },
    'mis':{
        'database': 'SwissProt',
        'taxonomy': 'All entries',
        'enzyme': 'Trypsin',
        'miscleavages': 1,
        'fixedMods': [],
        'variableMods': [],
        'precursorMass': '',
        'peptideTol': 1.0,
        'peptideTolUnits': 'Da',
        'msmsTol': 0.5,
        'msmsTolUnits': 'Da',
        'massType': 'Average',
        'charge': '1+',
        'instrument': 'Default',
        'quantitation': 'None',
        'decoy': 0,
        'errorTolerant': 0,
        'report': 'AUTO',
    },
}

links={
    'biomedmstools': 'http://ms.biomed.cas.cz/MSTools/',
    'blast': 'http://www.ebi.ac.uk/Tools/blastall/',
    'clustalw': 'http://www.ebi.ac.uk/Tools/clustalw/',
    'deltamass': 'http://www.abrf.org/index.cfm/dm.home',
    'emblebi': 'http://www.ebi.ac.uk/services/',
    'expasy': 'http://www.expasy.org/',
    'fasta': 'http://www.ebi.ac.uk/Tools/fasta33/',
    'matrixscience': 'http://www.matrixscience.com/',
    'muscle': 'http://phylogenomics.berkeley.edu/cgi-bin/muscle/input_muscle.py',
    'ncbi': 'http://www.ncbi.nlm.nih.gov/Entrez/',
    'pdb': 'http://www.rcsb.org/pdb/',
    'pir': 'http://pir.georgetown.edu/',
    'profound': 'http://prowl.rockefeller.edu/prowl-cgi/profound.exe',
    'prospector': 'http://prospector.ucsf.edu/',
    'unimod': 'http://www.unimod.org/',
    'uniprot': 'http://www.uniprot.org/',
}

methods={
    'processing':{
        'ESI-ICR Peptides':{
            'crop':{
                'lowMass': 200,
                'highMass': 4000,
            },
            'smoothing':{
                'method': 'SG',
                'windowSize': 0.05,
                'cycles': 1,
            },
            'baseline':{
                'segments': 15,
                'offset': 0,
                'smooth': 1,
            },
            'peakpicking':{
                'peakWidth': 0.1,
                'snTreshold': 4,
                'absIntTreshold': 0,
                'relIntTreshold': 0.001,
                'smoothing': 0,
                'pickingHeight': 0.85,
                'adaptiveNoise': 0,
                'deisotoping': 1,
            },
            'deisotoping':{
                'maxCharge': 5,
                'massTolerance': 0.02,
                'intTolerance': 0.5,
                'removeIsotopes': 1,
                'removeUnknown': 1,
            },
        },
        'MALDI-TOF Peptides':{
            'crop':{
                'lowMass': 750,
                'highMass': 4000,
            },
            'smoothing':{
                'method': 'SG',
                'windowSize': 0.2,
                'cycles': 3,
            },
            'baseline':{
                'segments': 15,
                'offset': 0,
                'smooth': 1,
            },
            'peakpicking':{
                'peakWidth': 0.25,
                'snTreshold': 3.5,
                'absIntTreshold': 0,
                'relIntTreshold': 0.005,
                'smoothing': 'SG',
                'pickingHeight': 0.75,
                'adaptiveNoise': 0,
                'deisotoping': 1,
            },
            'deisotoping':{
                'maxCharge': 1,
                'massTolerance': 0.15,
                'intTolerance': 0.5,
                'removeIsotopes': 1,
                'removeUnknown': 1,
            },
        },
        'MALDI-TOF Proteins 5-20 kDa':{
            'crop':{
                'lowMass': 5000,
                'highMass': 20000,
            },
            'smoothing':{
                'method': 'MA',
                'windowSize': 3,
                'cycles': 2,
            },
            'baseline':{
                'segments': 20,
                'offset': 0,
                'smooth': 1,
            },
            'peakpicking':{
                'peakWidth': 15,
                'snTreshold': 2,
                'absIntTreshold': 0,
                'relIntTreshold': 0.01,
                'smoothing': 'MA',
                'pickingHeight': 0.75,
                'adaptiveNoise': 1,
                'deisotoping': 0,
            },
            'deisotoping':{
                'maxCharge': 1,
                'massTolerance': 0.1,
                'intTolerance': 0.5,
                'removeIsotopes': 0,
                'removeUnknown': 0,
            },
        },
        'MALDI-TOF PSD':{
            'crop':{
                'lowMass': 0,
                'highMass': 4000,
            },
            'smoothing':{
                'method': 'SG',
                'windowSize': 0.7,
                'cycles': 2,
            },
            'baseline':{
                'segments': 100,
                'offset': 0,
                'smooth': 1,
            },
            'peakpicking':{
                'peakWidth': 0.7,
                'snTreshold': 3,
                'absIntTreshold': 0,
                'relIntTreshold': 0.005,
                'smoothing': 'SG',
                'pickingHeight': 0.75,
                'adaptiveNoise': 1,
                'deisotoping': 1,
            },
            'deisotoping':{
                'maxCharge': 1,
                'massTolerance': 0.2,
                'intTolerance': 0.5,
                'removeIsotopes': 1,
                'removeUnknown': 0,
            },
        },
        'MALDI-ICR Peptides':{
            'crop':{
                'lowMass': 750,
                'highMass': 4000,
            },
            'smoothing':{
                'method': 'SG',
                'windowSize': 0.05,
                'cycles': 1,
            },
            'baseline':{
                'segments': 15,
                'offset': 0,
                'smooth': 1,
            },
            'peakpicking':{
                'peakWidth': 0.1,
                'snTreshold': 4,
                'absIntTreshold': 0,
                'relIntTreshold': 0.001,
                'smoothing': 0,
                'pickingHeight': 0.85,
                'adaptiveNoise': 0,
                'deisotoping': 1,
            },
            'deisotoping':{
                'maxCharge': 1,
                'massTolerance': 0.02,
                'intTolerance': 0.5,
                'removeIsotopes': 1,
                'removeUnknown': 1,
            },
        },
    },
}

references={
    'PepMix Bruker - MALDI Pos Mo':[
        ('Bradykinin (1-7) [M+H]+', 757.399150),
        ('Angiotensin II [M+H]+', 1046.541792),
        ('Angiotensin I [M+H]+', 1296.684768),
        ('Substance P [M+H]+', 1347.735423),
        ('Bombesin [M+H]+', 1619.822341),
        ('ACTH clip (1-17) [M+H]+', 2093.086160),
        ('ACTH clip (18-39) [M+H]+', 2465.198332),
        ('Somatostatin 28 [M+H]+', 3147.470975),
    ],
    'PepMix Bruker - MALDI Neg Mo':[
        ('Angiotensin II [M-H]-', 1044.527247),
        ('Angiotensin I [M-H]-', 1294.670247),
        ('Substance P [M-H]-', 1345.720847),
        ('Bombesin [M-H]-', 1617.807747),
        ('ACTH clip (1-17) [M-H]-', 2091.071647),
        ('ACTH clip (18-39) [M-H]-', 2463.183747),
        ('Somatostatin 28 [M-H]-', 3145.456447),
    ],
    'PepMix Bruker PAC - MALDI Pos Mo':[
        ('Bradykinin (1-7) [M+H]+', 757.399160),
        ('Angiotensin III [M+H]+', 931.514849),
        ('Angiotensin II [M+H]+', 1046.541792),
        ('Angiotensin I [M+H]+', 1296.684768),
        ('Substance P [M+H]+', 1347.735423),
        ('Bombesin [M+H]+', 1619.822341),
        ('Neurotensin [M+H]+', 1672.917000),
        ('Renin Substrate [M+H]+', 1758.932610),
        ('ACTH clip (1-17) [M+H]+', 2093.086160),
        ('ACTH clip (18-39) [M+H]+', 2465.198332),
        ('ACTH clip (1-24) [M+H]+', 2932.587870),
        ('Somatostatin 28 [M+H]+', 3147.470975),
        ('ACTH clip (7-38) [M+H]+', 3657.928900),
    ],
    'ProtMix I Bruker - MALDI Pos Av':[
        ('Insulin [M+H]+', 5735),
        ('Cytochrome C [M+2H]2+', 6181),
        ('Myoglobin [M+2H]2+', 8477),
        ('Ubiquitin I [M+H]+', 8566),
        ('Cytochrom C [M+H]+', 12361),
        ('Myoglobin [M+H]+', 16953),
    ],
    'ProtMix I Bruker - MALDI Neg Av':[
        ('Insulin [M-H]-', 5733),
        ('Cytochrome C [M-2H]2-', 6179),
        ('Myoglobin [M-2H]2-', 8475),
        ('Ubiquitin I [M-H]-', 8564),
        ('Cytochrom C [M-H]-', 12359),
        ('Myoglobin [M-H]-', 16951),
    ],
    'ProtMix II Bruker - MALDI Pos Av':[
        ('Trypsinogen [M+H]+', 23982),
        ('Protein A [M+2H]2+', 22306),
        ('Albumin Bovine [M+2H]2+', 33216),
        ('Protein A [M+H]+', 44613),
        ('Albumin Bovine [M+H]+', 66431),
    ],
    'ProtMix II Bruker - MALDI Neg Av':[
        ('Trypsinogen [M+H]+', 23980),
        ('Protein A [M+2H]2+', 22304),
        ('Albumin Bovine [M+2H]2+', 33214),
        ('Protein A [M+H]+', 44611),
        ('Albumin Bovine [M+H]+', 66429),
    ],
    'Trypsin Promega (Porcine) - MALDI Pos Mo':[
        ('Trypsin (108-115) [M+H]+', 842.5094),
        ('Trypsin (209-216) [M+H]+', 906.5044),
        ('Trypsin (1-8) [M+H]+', 952.3894),
        ('Trypsin (148-157) [M+H]+', 1006.4874),
        ('Trypsin (98-107) [M+H]+', 1045.5637),
        ('Trypsin (134-147) [M+H]+', 1469.7305),
        ('Trypsin (58-72) [M+H]+', 1713.8084),
        ('Trypsin (217-231) [M+H]+', 1736.8425),
        ('Trypsin (116-133) [M+H]+', 1768.7993),
        ('Trypsin (62-77) [M+H]+', 1774.8975),
        ('Trypsin (58-76) [M+H]+', 2083.0096),
        ('Trypsin (158-178) [M+H]+', 2158.0307),
        ('Trypsin (58-77) [M+H]+', 2211.1040),
        ('Trypsin (78-97) [M+H]+', 2283.1802),
        ('Trypsin (179-208) [M+H]+', 3013.3237),
    ],
    'Trypsin Roche (Bovine) - MALDI Pos Mo':[
        ('Trypsin (112-119) [M+H]+', 805.4163),
        ('Trypsin (160-169) [M+H]+', 1020.503),
        ('Trypsin (229-237) [M+H]+', 1111.5605),
        ('Trypsin (207-220) [M+H]+', 1433.7206),
        ('Trypsin (70-89) [M+H]+', 2163.0564),
        ('Trypsin (90-109) [M+H]+', 2273.1595),
    ],
    'Trypsin Roche (Porcine) - MALDI Pos Mo':[
        ('Trypsin (108-115) [M+H]+', 842.5094),
        ('Trypsin (134-147) [M+H]+', 1469.7305),
        ('Trypsin (58-74) [M+H]+', 1940.9354),
        ('Trypsin (116-133) [M+H]+', 1768.7993),
        ('Trypsin (98-107) [M+H]+', 1045.5637),
        ('Trypsin (58-77) [M+H]+', 2211.104),
        ('Trypsin (148-157) [M+H]+', 1006.4874),
    ],
    'Keratin - MALDI Pos Mo':[
        ('Keratin 10 [M+H]+', 1165.5853),
        ('Keratin 1/II [M+H]+', 1179.6010),
        ('Keratin 1/II [M+H]+', 1300.5302),
        ('Keratin 1/II [M+H]+', 1716.8517),
        ('Keratin 1/II [M+H]+', 1993.9767),
        ('Keratin 1 [M+H]+', 2383.9520),
        ('Keratin 10 [M+H]+', 2825.4056),
    ],
    'HCCA Clusters - MALDI Pos Mo':[
        ('HCCA [M+H-H2O]+', 172.039304),
        ('HCCA [M+H]+', 190.049869),
        ('HCCA [M+Na-H2O]+', 194.021249),
        ('HCCA [M+Na]+', 212.031814),
        ('HCCA [M+K-H2O]+', 209.995186),
        ('HCCA [M+K]+', 228.005751),
        ('HCCA [2M+H-H2O]+', 361.081897),
        ('HCCA [2M+H]+', 379.092462),
        ('HCCA [2M+Na-H2O]+', 383.063842),
        ('HCCA [2M+Na]+', 401.074407),
        ('HCCA [2M+K-H2O]+', 399.037779),
        ('HCCA [2M+K]+', 417.048344),
        ('HCCA [2M+K+Na-H2O]+', 422.027),
        ('HCCA [3M+H-H2O]+', 550.12449),
        ('HCCA [3M+H]+', 568.135055),
        ('HCCA [3M+Na-H2O]+', 572.106435),
        ('HCCA [3M+Na]+', 590.117),
        ('HCCA [3M+K-H2O]+', 588.080372),
        ('HCCA [3M+K]+', 606.090937),
        ('HCCA [3M+K+Na-H2O]+', 611.069593),
        ('HCCA [4M+H-H2O]+', 739.167083),
        ('HCCA [4M+H]+', 757.177648),
        ('HCCA [4M+Na-H2O]+', 761.149028),
        ('HCCA [4M+Na]+', 779.159593),
        ('HCCA [4M+K-H2O]+', 777.122965),
        ('HCCA [4M+K]+', 795.13353),
        ('HCCA [4M+K+Na-H2O]+', 800.112186),
        ('HCCA [5M+H-H2O]+', 928.209676),
        ('HCCA [5M+H]+', 946.220241),
        ('HCCA [5M+Na-H2O]+', 950.191621),
        ('HCCA [5M+Na]+', 968.202186),
        ('HCCA [5M+K-H2O]+', 966.165558),
        ('HCCA [5M+K]+', 984.176123),
        ('HCCA [5M+K+Na-H2O]+', 989.154779),
        ('HCCA [6M+H-H2O]+', 1117.252269),
        ('HCCA [6M+H]+', 1135.262834),
        ('HCCA [6M+Na-H2O]+', 1139.234214),
        ('HCCA [6M+Na]+', 1157.244779),
        ('HCCA [6M+K-H2O]+', 1155.208151),
        ('HCCA [6M+K]+', 1173.218716),
        ('HCCA [6M+K+Na-H2O]+', 1178.197372),
        ('HCCA [7M+H-H2O]+', 1306.294862),
        ('HCCA [7M+H]+', 1324.305427),
        ('HCCA [7M+Na-H2O]+', 1328.276807),
        ('HCCA [7M+Na]+', 1346.287372),
        ('HCCA [7M+K-H2O]+', 1344.250744),
        ('HCCA [7M+K]+', 1362.261309),
        ('HCCA [7M+K+Na-H2O]+', 1367.239965),
    ],
    'DHB Clusters - MALDI Pos Mo':[
        ('DHB [M+H-H2O]+', 137.02332),
        ('DHB [M+H]+', 155.033885),
        ('DHB [M+Na-H2O]+', 159.005265),
        ('DHB [M+Na]+', 177.01583),
        ('DHB [M+K-H2O]+', 174.979202),
        ('DHB [M+K]+', 192.989767),
        ('DHB [2M+H-H2O]+', 291.049929),
        ('DHB [2M+H]+', 309.060494),
        ('DHB [2M+Na-H2O]+', 313.031874),
        ('DHB [2M+Na]+', 331.042439),
        ('DHB [2M+K-H2O]+', 329.005811),
        ('DHB [2M+K]+', 347.016376),
        ('DHB [2M+K+Na-H2O]+', 351.995032),
        ('DHB [3M+H-H2O]+', 445.076538),
        ('DHB [3M+H]+', 463.087103),
        ('DHB [3M+Na-H2O]+', 467.058483),
        ('DHB [3M+Na]+', 485.069048),
        ('DHB [3M+K-H2O]+', 483.03242),
        ('DHB [3M+K]+', 501.042985),
        ('DHB [3M+K+Na-H2O]+', 506.021641),
        ('DHB [4M+H-H2O]+', 599.103147),
        ('DHB [4M+H]+', 617.113712),
        ('DHB [4M+Na-H2O]+', 621.085092),
        ('DHB [4M+Na]+', 639.095657),
        ('DHB [4M+K-H2O]+', 637.059029),
        ('DHB [4M+K]+', 655.069594),
        ('DHB [4M+K+Na-H2O]+', 660.04825),
        ('DHB [5M+H-H2O]+', 753.129756),
        ('DHB [5M+H]+', 771.140321),
        ('DHB [5M+Na-H2O]+', 775.111701),
        ('DHB [5M+Na]+', 793.122266),
        ('DHB [5M+K-H2O]+', 791.085638),
        ('DHB [5M+K]+', 809.096203),
        ('DHB [5M+K+Na-H2O]+', 814.074859),
        ('DHB [6M+H-H2O]+', 907.156365),
        ('DHB [6M+H]+', 925.16693),
        ('DHB [6M+Na-H2O]+', 929.13831),
        ('DHB [6M+Na]+', 947.148875),
        ('DHB [6M+K-H2O]+', 945.112247),
        ('DHB [6M+K]+', 963.122812),
        ('DHB [6M+K+Na-H2O]+', 968.101468),
        ('DHB [7M+H-H2O]+', 1061.182974),
        ('DHB [7M+H]+', 1079.193539),
        ('DHB [7M+Na-H2O]+', 1083.164919),
        ('DHB [7M+Na]+', 1101.175484),
        ('DHB [7M+K-H2O]+', 1099.138856),
        ('DHB [7M+K]+', 1117.149421),
        ('DHB [7M+K+Na-H2O]+', 1122.128077),
    ],
    'PEG - MALDI Pos':[
        ('C6H15O4 [M+H]+', 151.096485),
        ('C6H14O4 [M+Na]+', 173.078430),
        ('C8H19O5 [M+H]+', 195.122700),
        ('C8H18O5 [M+Na]+', 217.104645),
        ('C10H23O6 [M+H]+', 239.148915),
        ('C10H22O6 [M+Na]+', 261.130860),
        ('C12H27O7 [M+H]+', 283.175130),
        ('C12H26O7 [M+Na]+', 305.157074),
        ('C14H31O8 [M+H]+', 327.201344),
        ('C14H30O8 [M+Na]+', 349.183289),
        ('C16H35O9 [M+H]+', 371.227559),
        ('C16H34O9 [M+Na]+', 393.209504),
        ('C18H39O10 [M+H]+', 415.253774),
        ('C18H38O10 [M+Na]+', 437.235719),
        ('C20H43O11 [M+H]+', 459.279989),
        ('C20H42O11 [M+Na]+', 481.261933),
        ('C22H47O12 [M+H]+', 503.306203),
        ('C22H46O12 [M+Na]+', 525.288148),
        ('C24H51O13 [M+H]+', 547.332418),
        ('C24H50O13 [M+Na]+', 569.314363),
        ('C26H55O14 [M+H]+', 591.358633),
        ('C26H54O14 [M+Na]+', 613.340578),
        ('C28H59O15 [M+H]+', 635.384848),
        ('C28H58O15 [M+Na]+', 657.366792),
        ('C30H62O16 [M+Na]+', 701.393007),
        ('C32H66O17 [M+Na]+', 745.419222),
        ('C34H70O18 [M+Na]+', 789.445437),
        ('C36H74O19 [M+Na]+', 833.471651),
        ('C38H78O20 [M+Na]+', 877.497866),
        ('C40H82O21 [M+Na]+', 921.524081),
        ('C42H86O22 [M+Na]+', 965.550296),
        ('C44H90O23 [M+Na]+', 1009.576510),
        ('C46H94O24 [M+Na]+', 1053.602725),
        ('C48H98O25 [M+Na]+', 1097.628940),
        ('C50H102O26 [M+Na]+', 1141.655155),
        ('C52H106O27 [M+Na]+', 1185.681369),
        ('C54H110O28 [M+Na]+', 1229.707584),
        ('C56H114O29 [M+Na]+', 1273.733799),
        ('C58H118O30 [M+Na]+', 1317.760014),
        ('C60H122O31 [M+Na]+', 1361.786228),
        ('C62H126O32 [M+Na]+', 1405.812443),
        ('C64H130O33 [M+Na]+', 1449.838658),
        ('C66H134O34 [M+Na]+', 1493.864873),
        ('C68H138O35 [M+Na]+', 1537.891087),
        ('C70H142O36 [M+Na]+', 1581.917302),
        ('C72H146O37 [M+Na]+', 1625.943517),
        ('C74H150O38 [M+Na]+', 1669.969732),
        ('C76H154O39 [M+Na]+', 1713.995946),
        ('C78H158O40 [M+Na]+', 1758.022161),
        ('C80H162O41 [M+Na]+', 1802.048376),
        ('C82H166O42 [M+Na]+', 1846.074591),
        ('C84H170O43 [M+Na]+', 1890.100805),
        ('C86H174O44 [M+Na]+', 1934.127020),
        ('C88H178O45 [M+Na]+', 1978.153235),
        ('C90H182O46 [M+Na]+', 2022.179450),
        ('C92H186O47 [M+Na]+', 2066.205664),
        ('C94H190O48 [M+Na]+', 2110.231879),
        ('C96H194O49 [M+Na]+', 2154.258094),
        ('C98H198O50 [M+Na]+', 2198.284309),
        ('C100H2O2O51 [M+Na]+', 2242.310523),
        ('C104H210O53 [M+Na]+', 2330.362953),
        ('C108H218O55 [M+Na]+', 2418.415382),
        ('C112H226O57 [M+Na]+', 2506.467812),
        ('C116H234O59 [M+Na]+', 2594.520241),
        ('C120H242O61 [M+Na]+', 2682.572671),
        ('C124H250O63 [M+Na]+', 2770.652100),
        ('C128H258O65 [M+Na]+', 2858.677530),
        ('C132H266O67 [M+Na]+', 2946.729959),
        ('C136H274O69 [M+Na]+', 3034.782389),
        ('C140H282O71 [M+Na]+', 3122.834828),
    ],
}


# LOADING FUNCTIONS
# -----------------

def loadConfig(path='configs/config.xml'):
    """Parse config XML and get data."""
    
    # parse XML
    document = xml.dom.minidom.parse(path)
    
    # main
    mainTags = document.getElementsByTagName('main')
    if mainTags:
        loadParams(mainTags[0], main)
    
    # recent files
    recentTags = document.getElementsByTagName('recent')
    if recentTags:
        pathTags = recentTags[0].getElementsByTagName('path')
        if pathTags:
            del recent[:]
            for pathTag in pathTags:
                recent.append(pathTag.getAttribute('value'))
    
    # colours
    coloursTags = document.getElementsByTagName('colours')
    if coloursTags:
        colourTags = coloursTags[0].getElementsByTagName('colour')
        if colourTags:
            del colours[:]
            for colourTag in colourTags:
                col = colourTag.getAttribute('value')
                colours.append([int(c, 16) for c in (col[0:2], col[2:4], col[4:6])])
    
    # export
    exportTags = document.getElementsByTagName('export')
    if exportTags:
        loadParams(exportTags[0], export)
        
        if type(export['peaklistColumns']) == str:
            export['peaklistColumns'] = export['peaklistColumns'].split(';')
    
    # spectrum
    spectrumTags = document.getElementsByTagName('spectrum')
    if spectrumTags:
        loadParams(spectrumTags[0], spectrum)
        
        if type(spectrum['tickColour']) == str:
            col = spectrum['tickColour']
            spectrum['tickColour'] = [int(c, 16) for c in (col[0:2], col[2:4], col[4:6])]
        
        if type(spectrum['tmpSpectrumColour']) == str:
            col = spectrum['tmpSpectrumColour']
            spectrum['tmpSpectrumColour'] = [int(c, 16) for c in (col[0:2], col[2:4], col[4:6])]
        
        if type(spectrum['matchPointsColour']) == str:
            col = spectrum['matchPointsColour']
            spectrum['matchPointsColour'] = [int(c, 16) for c in (col[0:2], col[2:4], col[4:6])]
    
    # match
    matchTags = document.getElementsByTagName('match')
    if matchTags:
        loadParams(matchTags[0], match)
    
    # processing
    processingTags = document.getElementsByTagName('processing')
    if processingTags:
        
        cropTags = processingTags[0].getElementsByTagName('crop')
        if cropTags:
            loadParams(cropTags[0], processing['crop'])
        
        smoothingTags = processingTags[0].getElementsByTagName('smoothing')
        if smoothingTags:
            loadParams(smoothingTags[0], processing['smoothing'])
        
        baselineTags = processingTags[0].getElementsByTagName('baseline')
        if baselineTags:
            loadParams(baselineTags[0], processing['baseline'])
        
        peakpickingTags = processingTags[0].getElementsByTagName('peakpicking')
        if peakpickingTags:
            loadParams(peakpickingTags[0], processing['peakpicking'])
        
        deisotopingTags = processingTags[0].getElementsByTagName('deisotoping')
        if deisotopingTags:
            loadParams(deisotopingTags[0], processing['deisotoping'])
    
    # calibration
    calibrationTags = document.getElementsByTagName('calibration')
    if calibrationTags:
        loadParams(calibrationTags[0], calibration)
    
    # sequence
    sequenceTags = document.getElementsByTagName('sequence')
    if sequenceTags:
        
        digestTags = sequenceTags[0].getElementsByTagName('digest')
        if digestTags:
            loadParams(digestTags[0], sequence['digest'])
        
        fragmentTags = sequenceTags[0].getElementsByTagName('fragment')
        if fragmentTags:
            loadParams(fragmentTags[0], sequence['fragment'])
        
        searchTags = sequenceTags[0].getElementsByTagName('search')
        if searchTags:
            loadParams(searchTags[0], sequence['search'])
        
        if type(sequence['fragment']['fragments']) == str:
            sequence['fragment']['fragments'] = sequence['fragment']['fragments'].split(';')
    
    # masscalc
    masscalcTags = document.getElementsByTagName('masscalc')
    if masscalcTags:
        loadParams(masscalcTags[0], masscalc)
    
    # differences
    differencesTags = document.getElementsByTagName('differences')
    if differencesTags:
        loadParams(differencesTags[0], differences)
    
    # mascot
    mascotTags = document.getElementsByTagName('mascot')
    if mascotTags:
        
        serverTags = mascotTags[0].getElementsByTagName('server')
        for serverTag in serverTags:
            name = serverTag.getAttribute('name')
            mascot['servers'][name] = {
                'host': '',
                'path': '/',
                'search': 'cgi/nph-mascot.exe',
                'results': 'cgi/master_results.pl',
                'export': 'cgi/export_dat_2.pl',
                'params': 'cgi/get_params.pl',
            }
            loadParams(serverTag, mascot['servers'][name])
        
        commonTags = mascotTags[0].getElementsByTagName('common')
        if commonTags:
            loadParams(commonTags[0], mascot['common'])
        
        pmfTags = mascotTags[0].getElementsByTagName('pmf')
        if pmfTags:
            loadParams(pmfTags[0], mascot['pmf'])
        
        sqTags = mascotTags[0].getElementsByTagName('sq')
        if sqTags:
            loadParams(sqTags[0], mascot['sq'])
        
        misTags = mascotTags[0].getElementsByTagName('mis')
        if misTags:
            loadParams(misTags[0], mascot['mis'])
        
        for key in ('pmf', 'sq', 'mis'):
            if type(mascot[key]['fixedMods']) == str:
                mascot[key]['fixedMods'] = mascot[key]['fixedMods'].split(';')
            if type(mascot[key]['variableMods']) == str:
                mascot[key]['variableMods'] = mascot[key]['variableMods'].split(';')
    
    # links
    linksTags = document.getElementsByTagName('links')
    if linksTags:
        linkTags = linksTags[0].getElementsByTagName('link')
        for linkTag in linkTags:
            name = linkTag.getAttribute('name')
            value = linkTag.getAttribute('value')
            links[name] = value
# ----


def loadMethods(path='configs/methods.xml'):
    """Parse processing methods XML and get data."""
    
    # parse XML
    document = xml.dom.minidom.parse(path)
    
    # get processing methods
    processingTags = document.getElementsByTagName('processing')
    if processingTags:
        methodTags = processingTags[0].getElementsByTagName('method')
        if methodTags:
            methods['processing'].clear()
            
            for methodTag in methodTags:
                name = methodTag.getAttribute('name')
                methods['processing'][name] = deepcopy(processing)
                
                cropTags = methodTag.getElementsByTagName('crop')
                if cropTags:
                    loadParams(cropTags[0], methods['processing'][name]['crop'])
                
                smoothingTags = methodTag.getElementsByTagName('smoothing')
                if smoothingTags:
                    loadParams(smoothingTags[0], methods['processing'][name]['smoothing'])
                
                baselineTags = methodTag.getElementsByTagName('baseline')
                if baselineTags:
                    loadParams(baselineTags[0], methods['processing'][name]['baseline'])
                
                peakpickingTags = methodTag.getElementsByTagName('peakpicking')
                if peakpickingTags:
                    loadParams(peakpickingTags[0], methods['processing'][name]['peakpicking'])
                
                deisotopingTags = methodTag.getElementsByTagName('deisotoping')
                if deisotopingTags:
                    loadParams(deisotopingTags[0], methods['processing'][name]['deisotoping'])
# ----


def loadReferences(path='configs/references.xml'):
    """Parse calibration references XML and get data."""
    
    # parse XML
    document = xml.dom.minidom.parse(path)
    
    # get references
    standardTags = document.getElementsByTagName('standard')
    if standardTags:
        references.clear()
        for standardTag in standardTags:
            standardName = standardTag.getAttribute('name')
            references[standardName] = []
            
            referenceTags = standardTag.getElementsByTagName('reference')
            if referenceTags:
                for referenceTag in referenceTags:
                    refName = referenceTag.getAttribute('name')
                    mass = referenceTag.getAttribute('mass')
                    references[standardName].append((refName, float(mass)))
# ----


def loadParams(sectionTag, section):
    """Get params from nodes."""
    
    if sectionTag:
        paramTags = sectionTag.getElementsByTagName('param')
        if paramTags:
            if paramTags:
                for paramTag in paramTags:
                    name = paramTag.getAttribute('name')
                    value = paramTag.getAttribute('value')
                    valueType = paramTag.getAttribute('type')
                    if name in section:
                        section[name] = eval(valueType+'(value)')
# ----



# SAVING FUNCTIONS
# ----------------

def saveConfig(path='configs/config.xml'):
    """Make and save config XML."""
    
    data = makeConfigXML()
    try:
        save = file(path, 'w')
        save.write(data.encode("utf-8"))
        save.close()
        return True
    except:
        return False
# ----


def saveMethods(path='configs/methods.xml'):
    """Make and save methods XML."""
    
    data = makeMethodsXML()
    try:
        save = file(path, 'w')
        save.write(data.encode("utf-8"))
        save.close()
        return True
    except:
        return False
# ----


def saveReferences(path='configs/references.xml'):
    """Make and save calibration references XML."""
    
    data = makeReferencesXML()
    try:
        save = file(path, 'w')
        save.write(data.encode("utf-8"))
        save.close()
        return True
    except:
        return False
# ----


def makeConfigXML():
    """Format config XML."""
    
    buff = '<?xml version="1.0" encoding="utf-8" ?>\n'
    buff += '<mMassConfig version="1.0">\n\n'
    
    # main
    buff += '  <main>\n'
    buff += '    <param name="appWidth" value="%d" type="int" />\n' % (main['appWidth'])
    buff += '    <param name="appHeight" value="%d" type="int" />\n' % (main['appHeight'])
    buff += '    <param name="appMaximized" value="%d" type="int" />\n' % (main['appMaximized'])
    buff += '    <param name="mzDigits" value="%d" type="int" />\n' % (main['mzDigits'])
    buff += '    <param name="intDigits" value="%d" type="int" />\n' % (main['intDigits'])
    buff += '    <param name="lastDir" value="%s" type="str" />\n' % (main['lastDir'])
    buff += '    <param name="errorUnits" value="%s" type="str" />\n' % (main['errorUnits'])
    buff += '    <param name="printQuality" value="%s" type="int" />\n' % (main['printQuality'])
    buff += '    <param name="macListCtrlGeneric" value="%s" type="int" />\n' % (main['macListCtrlGeneric'])
    buff += '  </main>\n\n'
    
    # recent files
    buff += '  <recent>\n'
    for item in recent:
        buff += '    <path value="%s" />\n' % (item)
    buff += '  </recent>\n\n'
    
    # colours
    buff += '  <colours>\n'
    for item in colours:
        buff += '    <colour value="%02x%02x%02x" />\n' % tuple(item)
    buff += '  </colours>\n\n'
    
    # export
    buff += '  <export>\n'
    buff += '    <param name="imageWidth" value="%.1f" type="float" />\n' % (export['imageWidth'])
    buff += '    <param name="imageHeight" value="%.1f" type="float" />\n' % (export['imageHeight'])
    buff += '    <param name="imageUnits" value="%s" type="str" />\n' % (export['imageUnits'])
    buff += '    <param name="imageResolution" value="%d" type="int" />\n' % (export['imageResolution'])
    buff += '    <param name="imageFormat" value="%s" type="str" />\n' % (export['imageFormat'])
    buff += '    <param name="peaklistColumns" value="%s" type="str" />\n' % (';'.join(export['peaklistColumns']))
    buff += '    <param name="peaklistFormat" value="%s" type="str" />\n' % (export['peaklistFormat'])
    buff += '    <param name="peaklistSeparator" value="%s" type="str" />\n' % (export['peaklistSeparator'])
    buff += '    <param name="spectrumSeparator" value="%s" type="str" />\n' % (export['spectrumSeparator'])
    buff += '  </export>\n\n'
    
    # spectrum
    buff += '  <spectrum>\n'
    buff += '    <param name="showGrid" value="%d" type="int" />\n' % (spectrum['showGrid'])
    buff += '    <param name="showLegend" value="%d" type="int" />\n' % (spectrum['showLegend'])
    buff += '    <param name="showPosBar" value="%d" type="int" />\n' % (spectrum['showPosBar'])
    buff += '    <param name="showGel" value="%d" type="int" />\n' % (spectrum['showGel'])
    buff += '    <param name="showGelLegend" value="%d" type="int" />\n' % (spectrum['showGelLegend'])
    buff += '    <param name="showTracker" value="%d" type="int" />\n' % (spectrum['showTracker'])
    buff += '    <param name="showLabels" value="%d" type="int" />\n' % (spectrum['showLabels'])
    buff += '    <param name="showAllLabels" value="%d" type="int" />\n' % (spectrum['showAllLabels'])
    buff += '    <param name="showTicks" value="%d" type="int" />\n' % (spectrum['showTicks'])
    buff += '    <param name="posBarHeight" value="%d" type="int" />\n' % (spectrum['posBarHeight'])
    buff += '    <param name="gelHeight" value="%d" type="int" />\n' % (spectrum['gelHeight'])
    buff += '    <param name="autoscale" value="%d" type="int" />\n' % (spectrum['autoscale'])
    buff += '    <param name="overlapLabels" value="%d" type="int" />\n' % (spectrum['overlapLabels'])
    buff += '    <param name="checkLimits" value="%d" type="int" />\n' % (spectrum['checkLimits'])
    buff += '    <param name="labelAngle" value="%d" type="int" />\n' % (spectrum['labelAngle'])
    buff += '    <param name="labelCharge" value="%d" type="int" />\n' % (spectrum['labelCharge'])
    buff += '    <param name="labelBgr" value="%d" type="int" />\n' % (spectrum['labelBgr'])
    buff += '    <param name="labelFontSize" value="%d" type="int" />\n' % (spectrum['labelFontSize'])
    buff += '    <param name="axisFontSize" value="%d" type="int" />\n' % (spectrum['axisFontSize'])
    buff += '    <param name="tickColour" value="%02x%02x%02x" type="str" />\n' % tuple(spectrum['tickColour'])
    buff += '    <param name="tmpSpectrumColour" value="%02x%02x%02x" type="str" />\n' % tuple(spectrum['tmpSpectrumColour'])
    buff += '    <param name="matchPointsColour" value="%02x%02x%02x" type="str" />\n' % tuple(spectrum['matchPointsColour'])
    buff += '  </spectrum>\n\n'
    
    # match
    buff += '  <match>\n'
    buff += '    <param name="tolerance" value="%f" type="float" />\n' % (match['tolerance'])
    buff += '    <param name="units" value="%s" type="str" />\n' % (match['units'])
    buff += '    <param name="ignoreCharge" value="%d" type="int" />\n' % (match['ignoreCharge'])
    buff += '  </match>\n\n'
    
    # processing
    buff += '  <processing>\n'
    buff += '    <crop>\n'
    buff += '      <param name="lowMass" value="%d" type="int" />\n' % (processing['crop']['lowMass'])
    buff += '      <param name="highMass" value="%d" type="int" />\n' % (processing['crop']['highMass'])
    buff += '    </crop>\n'
    buff += '    <smoothing>\n'
    buff += '      <param name="method" value="%s" type="str" />\n' % (processing['smoothing']['method'])
    buff += '      <param name="windowSize" value="%f" type="float" />\n' % (processing['smoothing']['windowSize'])
    buff += '      <param name="cycles" value="%d" type="int" />\n' % (processing['smoothing']['cycles'])
    buff += '    </smoothing>\n'
    buff += '    <baseline>\n'
    buff += '      <param name="segments" value="%d" type="int" />\n' % (processing['baseline']['segments'])
    buff += '      <param name="offset" value="%f" type="float" />\n' % (processing['baseline']['offset'])
    buff += '      <param name="smooth" value="%d" type="int" />\n' % (processing['baseline']['smooth'])
    buff += '    </baseline>\n'
    buff += '    <peakpicking>\n'
    buff += '      <param name="peakWidth" value="%f" type="float" />\n' % (processing['peakpicking']['peakWidth'])
    buff += '      <param name="snTreshold" value="%f" type="float" />\n' % (processing['peakpicking']['snTreshold'])
    buff += '      <param name="absIntTreshold" value="%f" type="float" />\n' % (processing['peakpicking']['absIntTreshold'])
    buff += '      <param name="relIntTreshold" value="%f" type="float" />\n' % (processing['peakpicking']['relIntTreshold'])
    buff += '      <param name="smoothing" value="%s" type="str" />\n' % (processing['peakpicking']['smoothing'])
    buff += '      <param name="pickingHeight" value="%f" type="float" />\n' % (processing['peakpicking']['pickingHeight'])
    buff += '      <param name="adaptiveNoise" value="%d" type="int" />\n' % (processing['peakpicking']['adaptiveNoise'])
    buff += '      <param name="deisotoping" value="%d" type="int" />\n' % (processing['peakpicking']['deisotoping'])
    buff += '    </peakpicking>\n'
    buff += '    <deisotoping>\n'
    buff += '      <param name="maxCharge" value="%d" type="int" />\n' % (processing['deisotoping']['maxCharge'])
    buff += '      <param name="massTolerance" value="%f" type="float" />\n' % (processing['deisotoping']['massTolerance'])
    buff += '      <param name="intTolerance" value="%f" type="float" />\n' % (processing['deisotoping']['intTolerance'])
    buff += '      <param name="removeIsotopes" value="%d" type="int" />\n' % (processing['deisotoping']['removeIsotopes'])
    buff += '      <param name="removeUnknown" value="%d" type="int" />\n' % (processing['deisotoping']['removeUnknown'])
    buff += '    </deisotoping>\n'
    buff += '  </processing>\n\n'
    
    # calibration
    buff += '  <calibration>\n'
    buff += '    <param name="fitting" value="%s" type="str" />\n' % (calibration['fitting'])
    buff += '    <param name="tolerance" value="%f" type="float" />\n' % (calibration['tolerance'])
    buff += '    <param name="units" value="%s" type="str" />\n' % (calibration['units'])
    buff += '    <param name="statCutOff" value="%d" type="int" />\n' % (calibration['statCutOff'])
    buff += '  </calibration>\n\n'
    
    # sequence
    buff += '  <sequence>\n'
    buff += '    <digest>\n'
    buff += '      <param name="maxMods" value="%d" type="int" />\n' % (sequence['digest']['maxMods'])
    buff += '      <param name="maxCharge" value="%d" type="int" />\n' % (sequence['digest']['maxCharge'])
    buff += '      <param name="massType" value="%d" type="int" />\n' % (sequence['digest']['massType'])
    buff += '      <param name="enzyme" value="%s" type="str" />\n' % (sequence['digest']['enzyme'])
    buff += '      <param name="miscl" value="%d" type="int" />\n' % (sequence['digest']['miscl'])
    buff += '      <param name="lowMass" value="%d" type="int" />\n' % (sequence['digest']['lowMass'])
    buff += '      <param name="highMass" value="%d" type="int" />\n' % (sequence['digest']['highMass'])
    buff += '      <param name="allowMods" value="%d" type="int" />\n' % (sequence['digest']['allowMods'])
    buff += '      <param name="listFormat" value="%s" type="str" />\n' % (sequence['digest']['listFormat'])
    buff += '      <param name="matchFormat" value="%s" type="str" />\n' % (sequence['digest']['matchFormat'])
    buff += '    </digest>\n'
    buff += '    <fragment>\n'
    buff += '      <param name="maxMods" value="%d" type="int" />\n' % (sequence['fragment']['maxMods'])
    buff += '      <param name="maxCharge" value="%d" type="int" />\n' % (sequence['fragment']['maxCharge'])
    buff += '      <param name="massType" value="%d" type="int" />\n' % (sequence['fragment']['massType'])
    buff += '      <param name="fragments" value="%s" type="str" />\n' % (';'.join(sequence['fragment']['fragments']))
    buff += '      <param name="filterFragments" value="%d" type="int" />\n' % (sequence['fragment']['filterFragments'])
    buff += '      <param name="listFormat" value="%s" type="str" />\n' % (sequence['fragment']['listFormat'])
    buff += '      <param name="matchFormat" value="%s" type="str" />\n' % (sequence['fragment']['matchFormat'])
    buff += '    </fragment>\n'
    buff += '    <search>\n'
    buff += '      <param name="maxMods" value="%d" type="int" />\n' % (sequence['search']['maxMods'])
    buff += '      <param name="maxCharge" value="%d" type="int" />\n' % (sequence['search']['maxCharge'])
    buff += '      <param name="massType" value="%d" type="int" />\n' % (sequence['search']['massType'])
    buff += '      <param name="enzyme" value="%s" type="str" />\n' % (sequence['search']['enzyme'])
    buff += '      <param name="tolerance" value="%f" type="float" />\n' % (sequence['search']['tolerance'])
    buff += '      <param name="units" value="%s" type="str" />\n' % (sequence['search']['units'])
    buff += '      <param name="listFormat" value="%s" type="str" />\n' % (sequence['search']['listFormat'])
    buff += '    </search>\n'
    buff += '  </sequence>\n\n'
    
    # masscalc
    buff += '  <masscalc>\n'
    buff += '    <param name="ionseriesAgent" value="%s" type="str" />\n' % (masscalc['ionseriesAgent'])
    buff += '    <param name="ionseriesAgentCharge" value="%d" type="int" />\n' % (masscalc['ionseriesAgentCharge'])
    buff += '    <param name="ionseriesPolarity" value="%d" type="int" />\n' % (masscalc['ionseriesPolarity'])
    buff += '    <param name="patternFwhm" value="%f" type="float" />\n' % (masscalc['patternFwhm'])
    buff += '    <param name="patternTreshold" value="%f" type="float" />\n' % (masscalc['patternTreshold'])
    buff += '  </masscalc>\n\n'
    
    # differences
    buff += '  <differences>\n'
    buff += '    <param name="aminoacids" value="%d" type="int" />\n' % (differences['aminoacids'])
    buff += '    <param name="dipeptides" value="%d" type="int" />\n' % (differences['dipeptides'])
    buff += '    <param name="tolerance" value="%f" type="float" />\n' % (differences['tolerance'])
    buff += '    <param name="massType" value="%d" type="int" />\n' % (differences['massType'])
    buff += '  </differences>\n\n'
    
    # mascot
    buff += '  <mascot>\n'
    buff += '    <servers>\n'
    for name in mascot['servers']:
        buff += '      <server name="%s">\n' % (name)
        buff += '        <param name="host" value="%s" type="str" />\n' % (mascot['servers'][name]['host'])
        buff += '        <param name="path" value="%s" type="str" />\n' % (mascot['servers'][name]['path'])
        buff += '        <param name="search" value="%s" type="str" />\n' % (mascot['servers'][name]['search'])
        buff += '        <param name="results" value="%s" type="str" />\n' % (mascot['servers'][name]['results'])
        buff += '        <param name="export" value="%s" type="str" />\n' % (mascot['servers'][name]['export'])
        buff += '        <param name="params" value="%s" type="str" />\n' % (mascot['servers'][name]['params'])
        buff += '      </server>\n'
    buff += '    </servers>\n'
    buff += '    <common>\n'
    buff += '      <param name="server" value="%s" type="str" />\n' % (mascot['common']['server'])
    buff += '      <param name="searchType" value="%s" type="str" />\n' % (mascot['common']['searchType'])
    buff += '      <param name="userName" value="%s" type="str" />\n' % (mascot['common']['userName'])
    buff += '      <param name="userEmail" value="%s" type="str" />\n' % (mascot['common']['userEmail'])
    buff += '    </common>\n'
    buff += '    <pmf>\n'
    buff += '      <param name="database" value="%s" type="str" />\n' % (mascot['pmf']['database'])
    buff += '      <param name="taxonomy" value="%s" type="str" />\n' % (mascot['pmf']['taxonomy'])
    buff += '      <param name="enzyme" value="%s" type="str" />\n' % (mascot['pmf']['enzyme'])
    buff += '      <param name="miscleavages" value="%s" type="str" />\n' % (mascot['pmf']['miscleavages'])
    buff += '      <param name="fixedMods" value="%s" type="str" />\n' % (';'.join(mascot['pmf']['fixedMods']))
    buff += '      <param name="variableMods" value="%s" type="str" />\n' % (';'.join(mascot['pmf']['variableMods']))
    buff += '      <param name="proteinMass" value="%s" type="str" />\n' % (mascot['pmf']['proteinMass'])
    buff += '      <param name="peptideTol" value="%s" type="str" />\n' % (mascot['pmf']['peptideTol'])
    buff += '      <param name="peptideTolUnits" value="%s" type="str" />\n' % (mascot['pmf']['peptideTolUnits'])
    buff += '      <param name="massType" value="%s" type="str" />\n' % (mascot['pmf']['massType'])
    buff += '      <param name="charge" value="%s" type="str" />\n' % (mascot['pmf']['charge'])
    buff += '      <param name="decoy" value="%d" type="int" />\n' % (mascot['pmf']['decoy'])
    buff += '      <param name="report" value="%s" type="str" />\n' % (mascot['pmf']['report'])
    buff += '    </pmf>\n'
    buff += '    <sq>\n'
    buff += '      <param name="database" value="%s" type="str" />\n' % (mascot['sq']['database'])
    buff += '      <param name="taxonomy" value="%s" type="str" />\n' % (mascot['sq']['taxonomy'])
    buff += '      <param name="enzyme" value="%s" type="str" />\n' % (mascot['sq']['enzyme'])
    buff += '      <param name="miscleavages" value="%s" type="str" />\n' % (mascot['sq']['miscleavages'])
    buff += '      <param name="fixedMods" value="%s" type="str" />\n' % (';'.join(mascot['sq']['fixedMods']))
    buff += '      <param name="variableMods" value="%s" type="str" />\n' % (';'.join(mascot['sq']['variableMods']))
    buff += '      <param name="peptideTol" value="%s" type="str" />\n' % (mascot['sq']['peptideTol'])
    buff += '      <param name="peptideTolUnits" value="%s" type="str" />\n' % (mascot['sq']['peptideTolUnits'])
    buff += '      <param name="msmsTol" value="%s" type="str" />\n' % (mascot['sq']['msmsTol'])
    buff += '      <param name="msmsTolUnits" value="%s" type="str" />\n' % (mascot['sq']['msmsTolUnits'])
    buff += '      <param name="massType" value="%s" type="str" />\n' % (mascot['sq']['massType'])
    buff += '      <param name="charge" value="%s" type="str" />\n' % (mascot['sq']['charge'])
    buff += '      <param name="instrument" value="%s" type="str" />\n' % (mascot['sq']['instrument'])
    buff += '      <param name="quantitation" value="%s" type="str" />\n' % (mascot['sq']['quantitation'])
    buff += '      <param name="decoy" value="%d" type="int" />\n' % (mascot['sq']['decoy'])
    buff += '      <param name="report" value="%s" type="str" />\n' % (mascot['sq']['report'])
    buff += '    </sq>\n'
    buff += '    <mis>\n'
    buff += '      <param name="database" value="%s" type="str" />\n' % (mascot['mis']['database'])
    buff += '      <param name="taxonomy" value="%s" type="str" />\n' % (mascot['mis']['taxonomy'])
    buff += '      <param name="enzyme" value="%s" type="str" />\n' % (mascot['mis']['enzyme'])
    buff += '      <param name="miscleavages" value="%s" type="str" />\n' % (mascot['mis']['miscleavages'])
    buff += '      <param name="fixedMods" value="%s" type="str" />\n' % (';'.join(mascot['mis']['fixedMods']))
    buff += '      <param name="variableMods" value="%s" type="str" />\n' % (';'.join(mascot['mis']['variableMods']))
    buff += '      <param name="precursorMass" value="%s" type="str" />\n' % (mascot['mis']['precursorMass'])
    buff += '      <param name="peptideTol" value="%s" type="str" />\n' % (mascot['mis']['peptideTol'])
    buff += '      <param name="peptideTolUnits" value="%s" type="str" />\n' % (mascot['mis']['peptideTolUnits'])
    buff += '      <param name="msmsTol" value="%s" type="str" />\n' % (mascot['mis']['msmsTol'])
    buff += '      <param name="msmsTolUnits" value="%s" type="str" />\n' % (mascot['mis']['msmsTolUnits'])
    buff += '      <param name="massType" value="%s" type="str" />\n' % (mascot['mis']['massType'])
    buff += '      <param name="charge" value="%s" type="str" />\n' % (mascot['mis']['charge'])
    buff += '      <param name="instrument" value="%s" type="str" />\n' % (mascot['mis']['instrument'])
    buff += '      <param name="quantitation" value="%s" type="str" />\n' % (mascot['mis']['quantitation'])
    buff += '      <param name="errorTolerant" value="%d" type="int" />\n' % (mascot['mis']['errorTolerant'])
    buff += '      <param name="decoy" value="%d" type="int" />\n' % (mascot['mis']['decoy'])
    buff += '      <param name="report" value="%s" type="str" />\n' % (mascot['mis']['report'])
    buff += '    </mis>\n'
    buff += '  </mascot>\n'
    
    # links
    buff += '  <links>\n'
    for name in links:
        buff += '    <link name="%s" value="%s" />\n' % (name, links[name])
    buff += '  </links>\n\n'
    
    buff += '</mMassConfig>'
    return buff
# ----


def makeMethodsXML():
    """Format proseccing method XML."""
    
    buff = '<?xml version="1.0" encoding="utf-8" ?>\n'
    buff += '<mMassMethods version="1.0">\n\n'
    
    # processing methods
    buff += '  <processing>\n\n'
    for name in sorted(methods['processing'].keys()):
        method = methods['processing'][name]
        buff += '    <method name="%s">\n' % (name)
        buff += '      <crop>\n'
        buff += '        <param name="lowMass" value="%d" type="int" />\n' % (method['crop']['lowMass'])
        buff += '        <param name="highMass" value="%d" type="int" />\n' % (method['crop']['highMass'])
        buff += '      </crop>\n'
        buff += '      <smoothing>\n'
        buff += '        <param name="method" value="%s" type="str" />\n' % (method['smoothing']['method'])
        buff += '        <param name="windowSize" value="%f" type="float" />\n' % (method['smoothing']['windowSize'])
        buff += '        <param name="cycles" value="%d" type="int" />\n' % (method['smoothing']['cycles'])
        buff += '      </smoothing>\n'
        buff += '      <baseline>\n'
        buff += '        <param name="segments" value="%d" type="int" />\n' % (method['baseline']['segments'])
        buff += '        <param name="offset" value="%f" type="float" />\n' % (method['baseline']['offset'])
        buff += '        <param name="smooth" value="%d" type="int" />\n' % (method['baseline']['smooth'])
        buff += '      </baseline>\n'
        buff += '      <peakpicking>\n'
        buff += '        <param name="peakWidth" value="%f" type="float" />\n' % (method['peakpicking']['peakWidth'])
        buff += '        <param name="snTreshold" value="%f" type="float" />\n' % (method['peakpicking']['snTreshold'])
        buff += '        <param name="absIntTreshold" value="%f" type="float" />\n' % (method['peakpicking']['absIntTreshold'])
        buff += '        <param name="relIntTreshold" value="%f" type="float" />\n' % (method['peakpicking']['relIntTreshold'])
        buff += '        <param name="smoothing" value="%s" type="str" />\n' % (method['peakpicking']['smoothing'])
        buff += '        <param name="pickingHeight" value="%f" type="float" />\n' % (method['peakpicking']['pickingHeight'])
        buff += '        <param name="adaptiveNoise" value="%d" type="int" />\n' % (method['peakpicking']['adaptiveNoise'])
        buff += '        <param name="deisotoping" value="%d" type="int" />\n' % (method['peakpicking']['deisotoping'])
        buff += '      </peakpicking>\n'
        buff += '      <deisotoping>\n'
        buff += '        <param name="maxCharge" value="%d" type="int" />\n' % (method['deisotoping']['maxCharge'])
        buff += '        <param name="massTolerance" value="%f" type="float" />\n' % (method['deisotoping']['massTolerance'])
        buff += '        <param name="intTolerance" value="%f" type="float" />\n' % (method['deisotoping']['intTolerance'])
        buff += '        <param name="removeIsotopes" value="%d" type="int" />\n' % (method['deisotoping']['removeIsotopes'])
        buff += '        <param name="removeUnknown" value="%d" type="int" />\n' % (method['deisotoping']['removeUnknown'])
        buff += '      </deisotoping>\n'
        buff += '    </method>\n\n'
    buff += '  </processing>\n\n'
    buff += '</mMassMethods>'
    return buff
# ----


def makeReferencesXML():
    """Format proseccing method XML."""
    
    buff = '<?xml version="1.0" encoding="utf-8" ?>\n'
    buff += '<mMassReferenceMasses version="1.0">\n\n'
    
    for name in sorted(references.keys()):
        buff += '  <standard name="%s">\n' % (name)
        for ref in references[name]:
            buff += '    <reference name="%s" mass="%f" />\n' % tuple(ref)
        buff += '  </standard>\n\n'
    
    buff += '</mMassReferenceMasses>'
    return buff
# ----



# LOAD USER CONFIG
# ----------------

try: loadConfig()
except IOError: saveConfig()
try: loadMethods()
except IOError: saveMethods()
try: loadReferences()
except IOError: saveReferences()