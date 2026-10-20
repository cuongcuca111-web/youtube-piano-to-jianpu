"""
Database of popular piano songs transcribed into accurate Jianpu notation
with both Right Hand (Melody) and Left Hand (Chords/Accompaniment).
"""

from typing import Dict, Any, List

SAMPLE_SONGS: Dict[str, Dict[str, Any]] = {
    "canon_in_d": {
        "id": "canon_in_d",
        "title": "Canon in D (Pachelbel's Canon)",
        "artist": "Johann Pachelbel",
        "keySignature": "1=D",
        "timeSignature": "4/4",
        "tempo": 74,
        "youtubeSampleUrl": "https://www.youtube.com/watch?v=Ptk_1Dc2iPY",
        "measures": [
            {
                "measureNumber": 1,
                "rightHand": [
                    {"number": "1", "octave": 1, "duration": 2.0, "display_text": "1̇", "midi": 74},
                    {"number": "7", "octave": 0, "duration": 2.0, "display_text": "7", "midi": 73}
                ],
                "leftHand": [
                    {"number": "1", "octave": -1, "duration": 2.0, "display_text": "1̣", "midi": 50},
                    {"number": "5", "octave": -2, "duration": 2.0, "display_text": "5̤", "midi": 45}
                ]
            },
            {
                "measureNumber": 2,
                "rightHand": [
                    {"number": "6", "octave": 0, "duration": 2.0, "display_text": "6", "midi": 71},
                    {"number": "5", "octave": 0, "duration": 2.0, "display_text": "5", "midi": 69}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 47},
                    {"number": "3", "octave": -2, "duration": 2.0, "display_text": "3̤", "midi": 42}
                ]
            },
            {
                "measureNumber": 3,
                "rightHand": [
                    {"number": "4", "octave": 0, "duration": 2.0, "display_text": "4", "midi": 67},
                    {"number": "3", "octave": 0, "duration": 2.0, "display_text": "3", "midi": 66}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 2.0, "display_text": "4̤", "midi": 43},
                    {"number": "1", "octave": -1, "duration": 2.0, "display_text": "1̣", "midi": 50}
                ]
            },
            {
                "measureNumber": 4,
                "rightHand": [
                    {"number": "4", "octave": 0, "duration": 2.0, "display_text": "4", "midi": 67},
                    {"number": "5", "octave": 0, "duration": 2.0, "display_text": "5", "midi": 69}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 2.0, "display_text": "4̤", "midi": 43},
                    {"number": "5", "octave": -2, "duration": 2.0, "display_text": "5̤", "midi": 45}
                ]
            },
            {
                "measureNumber": 5,
                "rightHand": [
                    {"number": "1", "octave": 1, "duration": 0.5, "display_text": "1̇", "midi": 74},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 73},
                    {"number": "1", "octave": 1, "duration": 0.5, "display_text": "1̇", "midi": 74},
                    {"number": "2", "octave": 1, "duration": 0.5, "display_text": "2̇", "midi": 76},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 73},
                    {"number": "6", "octave": 0, "duration": 0.5, "display_text": "6", "midi": 71},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 73},
                    {"number": "1", "octave": 1, "duration": 0.5, "display_text": "1̇", "midi": 74}
                ],
                "leftHand": [
                    {"number": "1", "octave": -1, "duration": 2.0, "display_text": "1̣", "midi": 50},
                    {"number": "5", "octave": -2, "duration": 2.0, "display_text": "5̤", "midi": 45}
                ]
            },
            {
                "measureNumber": 6,
                "rightHand": [
                    {"number": "6", "octave": 0, "duration": 0.5, "display_text": "6", "midi": 71},
                    {"number": "5", "octave": 0, "duration": 0.5, "display_text": "5", "midi": 69},
                    {"number": "6", "octave": 0, "duration": 0.5, "display_text": "6", "midi": 71},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 73},
                    {"number": "5", "octave": 0, "duration": 0.5, "display_text": "5", "midi": 69},
                    {"number": "4", "octave": 0, "duration": 0.5, "display_text": "4", "midi": 67},
                    {"number": "5", "octave": 0, "duration": 0.5, "display_text": "5", "midi": 69},
                    {"number": "6", "octave": 0, "duration": 0.5, "display_text": "6", "midi": 71}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 47},
                    {"number": "3", "octave": -2, "duration": 2.0, "display_text": "3̤", "midi": 42}
                ]
            },
            {
                "measureNumber": 7,
                "rightHand": [
                    {"number": "4", "octave": 0, "duration": 0.5, "display_text": "4", "midi": 67},
                    {"number": "3", "octave": 0, "duration": 0.5, "display_text": "3", "midi": 66},
                    {"number": "4", "octave": 0, "duration": 0.5, "display_text": "4", "midi": 67},
                    {"number": "5", "octave": 0, "duration": 0.5, "display_text": "5", "midi": 69},
                    {"number": "3", "octave": 0, "duration": 0.5, "display_text": "3", "midi": 66},
                    {"number": "2", "octave": 0, "duration": 0.5, "display_text": "2", "midi": 64},
                    {"number": "3", "octave": 0, "duration": 0.5, "display_text": "3", "midi": 66},
                    {"number": "4", "octave": 0, "duration": 0.5, "display_text": "4", "midi": 67}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 2.0, "display_text": "4̤", "midi": 43},
                    {"number": "1", "octave": -1, "duration": 2.0, "display_text": "1̣", "midi": 50}
                ]
            },
            {
                "measureNumber": 8,
                "rightHand": [
                    {"number": "4", "octave": 0, "duration": 0.5, "display_text": "4", "midi": 67},
                    {"number": "5", "octave": 0, "duration": 0.5, "display_text": "5", "midi": 69},
                    {"number": "6", "octave": 0, "duration": 0.5, "display_text": "6", "midi": 71},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 73},
                    {"number": "1", "octave": 1, "duration": 2.0, "display_text": "1̇", "midi": 74}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 2.0, "display_text": "4̤", "midi": 43},
                    {"number": "5", "octave": -2, "duration": 2.0, "display_text": "5̤", "midi": 45}
                ]
            }
        ]
    },

    "fur_elise": {
        "id": "fur_elise",
        "title": "Für Elise (Bagatelle No. 25)",
        "artist": "Ludwig van Beethoven",
        "keySignature": "1=C",
        "timeSignature": "3/8",
        "tempo": 128,
        "youtubeSampleUrl": "https://www.youtube.com/watch?v=_4IRMYuE1hI",
        "measures": [
            {
                "measureNumber": 1,
                "rightHand": [
                    {"number": "3", "octave": 1, "duration": 0.5, "display_text": "3̇", "midi": 76},
                    {"number": "2", "octave": 1, "accidental": "#", "duration": 0.5, "display_text": "#2̇", "midi": 75},
                    {"number": "3", "octave": 1, "duration": 0.5, "display_text": "3̇", "midi": 76}
                ],
                "leftHand": [
                    {"number": "0", "octave": 0, "duration": 1.5, "display_text": "0", "midi": 0}
                ]
            },
            {
                "measureNumber": 2,
                "rightHand": [
                    {"number": "2", "octave": 1, "accidental": "#", "duration": 0.5, "display_text": "#2̇", "midi": 75},
                    {"number": "3", "octave": 1, "duration": 0.5, "display_text": "3̇", "midi": 76},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 71}
                ],
                "leftHand": [
                    {"number": "0", "octave": 0, "duration": 1.5, "display_text": "0", "midi": 0}
                ]
            },
            {
                "measureNumber": 3,
                "rightHand": [
                    {"number": "2", "octave": 1, "duration": 0.5, "display_text": "2̇", "midi": 74},
                    {"number": "1", "octave": 1, "duration": 0.5, "display_text": "1̇", "midi": 72},
                    {"number": "6", "octave": 0, "duration": 1.0, "display_text": "6", "midi": 69}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 0.5, "display_text": "6̤", "midi": 45},
                    {"number": "3", "octave": -1, "duration": 0.5, "display_text": "3̣", "midi": 52},
                    {"number": "6", "octave": -1, "duration": 0.5, "display_text": "6̣", "midi": 57}
                ]
            },
            {
                "measureNumber": 4,
                "rightHand": [
                    {"number": "0", "octave": 0, "duration": 0.5, "display_text": "0", "midi": 0},
                    {"number": "1", "octave": 0, "duration": 0.5, "display_text": "1", "midi": 60},
                    {"number": "3", "octave": 0, "duration": 0.5, "display_text": "3", "midi": 64}
                ],
                "leftHand": [
                    {"number": "0", "octave": 0, "duration": 1.5, "display_text": "0", "midi": 0}
                ]
            },
            {
                "measureNumber": 5,
                "rightHand": [
                    {"number": "6", "octave": 0, "duration": 0.5, "display_text": "6", "midi": 69},
                    {"number": "7", "octave": 0, "duration": 1.0, "display_text": "7", "midi": 71}
                ],
                "leftHand": [
                    {"number": "3", "octave": -2, "duration": 0.5, "display_text": "3̤", "midi": 40},
                    {"number": "7", "octave": -2, "duration": 0.5, "display_text": "7̤", "midi": 47},
                    {"number": "3", "octave": -1, "duration": 0.5, "display_text": "3̣", "midi": 52}
                ]
            },
            {
                "measureNumber": 6,
                "rightHand": [
                    {"number": "0", "octave": 0, "duration": 0.5, "display_text": "0", "midi": 0},
                    {"number": "3", "octave": 0, "duration": 0.5, "display_text": "3", "midi": 64},
                    {"number": "5", "octave": 0, "accidental": "#", "duration": 0.5, "display_text": "#5", "midi": 68}
                ],
                "leftHand": [
                    {"number": "0", "octave": 0, "duration": 1.5, "display_text": "0", "midi": 0}
                ]
            },
            {
                "measureNumber": 7,
                "rightHand": [
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 71},
                    {"number": "1", "octave": 1, "duration": 1.0, "display_text": "1̇", "midi": 72}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 0.5, "display_text": "6̤", "midi": 45},
                    {"number": "3", "octave": -1, "duration": 0.5, "display_text": "3̣", "midi": 52},
                    {"number": "6", "octave": -1, "duration": 0.5, "display_text": "6̣", "midi": 57}
                ]
            }
        ]
    },

    "river_flows_in_you": {
        "id": "river_flows_in_you",
        "title": "River Flows in You",
        "artist": "Yiruma",
        "keySignature": "1=A",
        "timeSignature": "4/4",
        "tempo": 70,
        "youtubeSampleUrl": "https://www.youtube.com/watch?v=7maJOI3QMu0",
        "measures": [
            {
                "measureNumber": 1,
                "rightHand": [
                    {"number": "3", "octave": 1, "duration": 0.5, "display_text": "3̇", "midi": 76},
                    {"number": "2", "octave": 1, "duration": 0.5, "display_text": "2̇", "midi": 74},
                    {"number": "3", "octave": 1, "duration": 0.5, "display_text": "3̇", "midi": 76},
                    {"number": "5", "octave": 1, "duration": 0.5, "display_text": "5̇", "midi": 79},
                    {"number": "1", "octave": 1, "duration": 2.0, "display_text": "1̇", "midi": 73}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 1.0, "display_text": "6̤", "midi": 45},
                    {"number": "3", "octave": -1, "duration": 1.0, "display_text": "3̣", "midi": 52},
                    {"number": "1", "octave": 0, "duration": 2.0, "display_text": "1", "midi": 61}
                ]
            },
            {
                "measureNumber": 2,
                "rightHand": [
                    {"number": "0", "octave": 0, "duration": 1.0, "display_text": "0", "midi": 0},
                    {"number": "1", "octave": 1, "duration": 0.5, "display_text": "1̇", "midi": 73},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 71},
                    {"number": "1", "octave": 1, "duration": 2.0, "display_text": "1̇", "midi": 73}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 1.0, "display_text": "4̤", "midi": 42},
                    {"number": "1", "octave": -1, "duration": 1.0, "display_text": "1̣", "midi": 49},
                    {"number": "6", "octave": -1, "duration": 2.0, "display_text": "6̣", "midi": 57}
                ]
            },
            {
                "measureNumber": 3,
                "rightHand": [
                    {"number": "3", "octave": 1, "duration": 0.5, "display_text": "3̇", "midi": 76},
                    {"number": "2", "octave": 1, "duration": 0.5, "display_text": "2̇", "midi": 74},
                    {"number": "3", "octave": 1, "duration": 0.5, "display_text": "3̇", "midi": 76},
                    {"number": "5", "octave": 1, "duration": 0.5, "display_text": "5̇", "midi": 79},
                    {"number": "1", "octave": 1, "duration": 2.0, "display_text": "1̇", "midi": 73}
                ],
                "leftHand": [
                    {"number": "1", "octave": -1, "duration": 1.0, "display_text": "1̣", "midi": 45},
                    {"number": "5", "octave": -1, "duration": 1.0, "display_text": "5̣", "midi": 52},
                    {"number": "3", "octave": 0, "duration": 2.0, "display_text": "3", "midi": 61}
                ]
            },
            {
                "measureNumber": 4,
                "rightHand": [
                    {"number": "0", "octave": 0, "duration": 1.0, "display_text": "0", "midi": 0},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 71},
                    {"number": "6", "octave": 0, "duration": 0.5, "display_text": "6", "midi": 69},
                    {"number": "5", "octave": 0, "duration": 2.0, "display_text": "5", "midi": 67}
                ],
                "leftHand": [
                    {"number": "5", "octave": -2, "duration": 1.0, "display_text": "5̤", "midi": 43},
                    {"number": "2", "octave": -1, "duration": 1.0, "display_text": "2̣", "midi": 50},
                    {"number": "7", "octave": -1, "duration": 2.0, "display_text": "7̣", "midi": 58}
                ]
            }
        ]
    },

    "gap_me_trong_mo": {
        "id": "gap_me_trong_mo",
        "title": "Gặp Mẹ Trong Mơ (Mother in the Dream)",
        "artist": "Uudam (Dân ca Mông Cổ)",
        "keySignature": "1=C",
        "timeSignature": "4/4",
        "tempo": 76,
        "youtubeSampleUrl": "https://www.youtube.com/watch?v=FjK3sVz0bA0",
        "measures": [
            {
                "measureNumber": 1,
                "rightHand": [
                    {"number": "6", "octave": 0, "duration": 1.0, "display_text": "6", "midi": 69},
                    {"number": "1", "octave": 1, "duration": 1.0, "display_text": "1̇", "midi": 72},
                    {"number": "2", "octave": 1, "duration": 1.0, "display_text": "2̇", "midi": 74},
                    {"number": "3", "octave": 1, "duration": 1.0, "display_text": "3̇", "midi": 76}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 4.0, "display_text": "6̤", "midi": 45}
                ]
            },
            {
                "measureNumber": 2,
                "rightHand": [
                    {"number": "2", "octave": 1, "duration": 3.0, "display_text": "2̇", "midi": 74},
                    {"number": "3", "octave": 1, "duration": 0.5, "display_text": "3̇", "midi": 76},
                    {"number": "2", "octave": 1, "duration": 0.5, "display_text": "2̇", "midi": 74}
                ],
                "leftHand": [
                    {"number": "2", "octave": -2, "duration": 4.0, "display_text": "2̤", "midi": 38}
                ]
            },
            {
                "measureNumber": 3,
                "rightHand": [
                    {"number": "1", "octave": 1, "duration": 1.0, "display_text": "1̇", "midi": 72},
                    {"number": "6", "octave": 0, "duration": 1.0, "display_text": "6", "midi": 69},
                    {"number": "5", "octave": 0, "duration": 2.0, "display_text": "5", "midi": 67}
                ],
                "leftHand": [
                    {"number": "5", "octave": -2, "duration": 4.0, "display_text": "5̤", "midi": 43}
                ]
            },
            {
                "measureNumber": 4,
                "rightHand": [
                    {"number": "6", "octave": 0, "duration": 4.0, "display_text": "6", "midi": 69}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 4.0, "display_text": "6̤", "midi": 45}
                ]
            },
            {
                "measureNumber": 5,
                "rightHand": [
                    {"number": "3", "octave": 1, "duration": 1.0, "display_text": "3̇", "midi": 76},
                    {"number": "5", "octave": 1, "duration": 1.0, "display_text": "5̇", "midi": 79},
                    {"number": "6", "octave": 1, "duration": 1.5, "display_text": "6̇", "midi": 81},
                    {"number": "5", "octave": 1, "duration": 0.5, "display_text": "5̇", "midi": 79}
                ],
                "leftHand": [
                    {"number": "1", "octave": -1, "duration": 4.0, "display_text": "1̣", "midi": 48}
                ]
            },
            {
                "measureNumber": 6,
                "rightHand": [
                    {"number": "3", "octave": 1, "duration": 3.0, "display_text": "3̇", "midi": 76},
                    {"number": "2", "octave": 1, "duration": 1.0, "display_text": "2̇", "midi": 74}
                ],
                "leftHand": [
                    {"number": "3", "octave": -2, "duration": 4.0, "display_text": "3̤", "midi": 40}
                ]
            },
            {
                "measureNumber": 7,
                "rightHand": [
                    {"number": "1", "octave": 1, "duration": 1.0, "display_text": "1̇", "midi": 72},
                    {"number": "6", "octave": 0, "duration": 1.0, "display_text": "6", "midi": 69},
                    {"number": "1", "octave": 1, "duration": 1.0, "display_text": "1̇", "midi": 72},
                    {"number": "2", "octave": 1, "duration": 1.0, "display_text": "2̇", "midi": 74}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 4.0, "display_text": "4̤", "midi": 41}
                ]
            },
            {
                "measureNumber": 8,
                "rightHand": [
                    {"number": "3", "octave": 1, "duration": 4.0, "display_text": "3̇", "midi": 76}
                ],
                "leftHand": [
                    {"number": "5", "octave": -2, "duration": 4.0, "display_text": "5̤", "midi": 43}
                ]
            }
        ]
    },

    "see_you_again": {
        "id": "see_you_again",
        "title": "See You Again (Piano Intro)",
        "artist": "Charlie Puth ft. Wiz Khalifa",
        "keySignature": "1=Bb",
        "timeSignature": "4/4",
        "tempo": 80,
        "youtubeSampleUrl": "https://www.youtube.com/watch?v=RgKAFK5djSk",
        "measures": [
            {
                "measureNumber": 1,
                "rightHand": [
                    {"number": "1", "octave": 1, "duration": 1.0, "display_text": "1̇", "midi": 70},
                    {"number": "2", "octave": 1, "duration": 1.0, "display_text": "2̇", "midi": 72},
                    {"number": "3", "octave": 1, "duration": 1.0, "display_text": "3̇", "midi": 74},
                    {"number": "5", "octave": 1, "duration": 1.0, "display_text": "5̇", "midi": 77}
                ],
                "leftHand": [
                    {"number": "1", "octave": -1, "duration": 4.0, "display_text": "1̣", "midi": 46}
                ]
            },
            {
                "measureNumber": 2,
                "rightHand": [
                    {"number": "6", "octave": 1, "duration": 2.0, "display_text": "6̇", "midi": 79},
                    {"number": "5", "octave": 1, "duration": 2.0, "display_text": "5̇", "midi": 77}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 4.0, "display_text": "6̤", "midi": 43}
                ]
            },
            {
                "measureNumber": 3,
                "rightHand": [
                    {"number": "3", "octave": 1, "duration": 1.0, "display_text": "3̇", "midi": 74},
                    {"number": "2", "octave": 1, "duration": 1.0, "display_text": "2̇", "midi": 72},
                    {"number": "1", "octave": 1, "duration": 2.0, "display_text": "1̇", "midi": 70}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 4.0, "display_text": "4̤", "midi": 39}
                ]
            },
            {
                "measureNumber": 4,
                "rightHand": [
                    {"number": "2", "octave": 1, "duration": 4.0, "display_text": "2̇", "midi": 72}
                ],
                "leftHand": [
                    {"number": "5", "octave": -2, "duration": 4.0, "display_text": "5̤", "midi": 41}
                ]
            }
        ]
    },
    "victory": {
        "id": "victory",
        "title": "Two Steps From Hell - Victory (Piano Tutorial)",
        "artist": "Thomas Bergersen (Two Steps From Hell)",
        "keySignature": "1=F",
        "timeSignature": "4/4",
        "tempo": 104,
        "youtubeSampleUrl": "https://www.youtube.com/watch?v=qySMrhVacQ8",
        "measures": [
            {
                "measureNumber": 1,
                "rightHand": [
                    {"number": "6", "octave": -1, "duration": 4.0, "display_text": "6̣", "midi": 62, "note_name": "D4"}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 50, "note_name": "D3"},
                    {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 50, "note_name": "D3"}
                ]
            },
            {
                "measureNumber": 2,
                "rightHand": [
                    {"number": "1", "octave": 0, "duration": 2.0, "display_text": "1", "midi": 65, "note_name": "F4"},
                    {"number": "2", "octave": 0, "duration": 1.0, "display_text": "2", "midi": 67, "note_name": "G4"},
                    {"number": "3", "octave": 0, "duration": 1.0, "display_text": "3", "midi": 69, "note_name": "A4"}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 50, "note_name": "D3"},
                    {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 50, "note_name": "D3"}
                ]
            },
            {
                "measureNumber": 3,
                "rightHand": [
                    {"number": "2", "octave": 0, "duration": 1.5, "display_text": "2", "midi": 67, "note_name": "G4"},
                    {"number": "1", "octave": 0, "duration": 0.5, "display_text": "1", "midi": 65, "note_name": "F4"},
                    {"number": "6", "octave": -1, "duration": 2.0, "display_text": "6̣", "midi": 62, "note_name": "D4"}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 2.0, "display_text": "4̤", "midi": 46, "note_name": "Bb2"},
                    {"number": "1", "octave": -1, "duration": 2.0, "display_text": "1̣", "midi": 53, "note_name": "F3"}
                ]
            },
            {
                "measureNumber": 4,
                "rightHand": [
                    {"number": "0", "octave": 0, "duration": 4.0, "display_text": "0", "midi": 0, "note_name": "Rest"}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 4.0, "display_text": "4̤", "midi": 46, "note_name": "Bb2"}
                ]
            },
            {
                "measureNumber": 5,
                "rightHand": [
                    {"number": "6", "octave": -1, "duration": 1.0, "display_text": "6̣", "midi": 62, "note_name": "D4"},
                    {"number": "1", "octave": 0, "duration": 1.0, "display_text": "1", "midi": 65, "note_name": "F4"},
                    {"number": "2", "octave": 0, "duration": 1.0, "display_text": "2", "midi": 67, "note_name": "G4"},
                    {"number": "3", "octave": 0, "duration": 1.0, "display_text": "3", "midi": 69, "note_name": "A4"}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 4.0, "display_text": "6̤", "midi": 50, "note_name": "D3"}
                ]
            },
            {
                "measureNumber": 6,
                "rightHand": [
                    {"number": "2", "octave": 0, "duration": 1.5, "display_text": "2", "midi": 67, "note_name": "G4"},
                    {"number": "1", "octave": 0, "duration": 0.5, "display_text": "1", "midi": 65, "note_name": "F4"},
                    {"number": "6", "octave": -1, "duration": 2.0, "display_text": "6̣", "midi": 62, "note_name": "D4"}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 4.0, "display_text": "4̤", "midi": 46, "note_name": "Bb2"}
                ]
            },
            {
                "measureNumber": 7,
                "rightHand": [
                    {"number": "3", "octave": 0, "duration": 1.0, "display_text": "3", "midi": 69, "note_name": "A4"},
                    {"number": "5", "octave": 0, "duration": 1.0, "display_text": "5", "midi": 72, "note_name": "C5"},
                    {"number": "6", "octave": 0, "duration": 2.0, "display_text": "6", "midi": 74, "note_name": "D5"}
                ],
                "leftHand": [
                    {"number": "1", "octave": -1, "duration": 4.0, "display_text": "1̣", "midi": 53, "note_name": "F3"}
                ]
            },
            {
                "measureNumber": 8,
                "rightHand": [
                    {"number": "5", "octave": 0, "duration": 1.5, "display_text": "5", "midi": 72, "note_name": "C5"},
                    {"number": "3", "octave": 0, "duration": 0.5, "display_text": "3", "midi": 69, "note_name": "A4"},
                    {"number": "2", "octave": 0, "duration": 2.0, "display_text": "2", "midi": 67, "note_name": "G4"}
                ],
                "leftHand": [
                    {"number": "5", "octave": -2, "duration": 4.0, "display_text": "5̤", "midi": 48, "note_name": "C3"}
                ]
            },
            {
                "measureNumber": 9,
                "rightHand": [
                    {"number": "3", "octave": 0, "duration": 1.0, "display_text": "3", "midi": 69, "note_name": "A4"},
                    {"number": "5", "octave": 0, "duration": 1.0, "display_text": "5", "midi": 72, "note_name": "C5"},
                    {"number": "6", "octave": 0, "duration": 1.0, "display_text": "6", "midi": 74, "note_name": "D5"},
                    {"number": "7", "octave": 0, "duration": 1.0, "display_text": "7", "midi": 76, "note_name": "E5"}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 4.0, "display_text": "6̤", "midi": 50, "note_name": "D3"}
                ]
            },
            {
                "measureNumber": 10,
                "rightHand": [
                    {"number": "1", "octave": 1, "duration": 1.5, "display_text": "1̇", "midi": 77, "note_name": "F5"},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 76, "note_name": "E5"},
                    {"number": "6", "octave": 0, "duration": 1.0, "display_text": "6", "midi": 74, "note_name": "D5"},
                    {"number": "5", "octave": 0, "duration": 1.0, "display_text": "5", "midi": 72, "note_name": "C5"}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 4.0, "display_text": "4̤", "midi": 46, "note_name": "Bb2"}
                ]
            },
            {
                "measureNumber": 11,
                "rightHand": [
                    {"number": "6", "octave": 0, "duration": 2.0, "display_text": "6", "midi": 74, "note_name": "D5"},
                    {"number": "5", "octave": 0, "duration": 1.0, "display_text": "5", "midi": 72, "note_name": "C5"},
                    {"number": "3", "octave": 0, "duration": 1.0, "display_text": "3", "midi": 69, "note_name": "A4"}
                ],
                "leftHand": [
                    {"number": "1", "octave": -1, "duration": 4.0, "display_text": "1̣", "midi": 53, "note_name": "F3"}
                ]
            },
            {
                "measureNumber": 12,
                "rightHand": [
                    {"number": "2", "octave": 0, "duration": 1.5, "display_text": "2", "midi": 67, "note_name": "G4"},
                    {"number": "3", "octave": 0, "duration": 0.5, "display_text": "3", "midi": 69, "note_name": "A4"},
                    {"number": "2", "octave": 0, "duration": 2.0, "display_text": "2", "midi": 67, "note_name": "G4"}
                ],
                "leftHand": [
                    {"number": "5", "octave": -2, "duration": 4.0, "display_text": "5̤", "midi": 48, "note_name": "C3"}
                ]
            },
            {
                "measureNumber": 13,
                "rightHand": [
                    {"number": "6", "octave": -1, "duration": 1.0, "display_text": "6̣", "midi": 62, "note_name": "D4"},
                    {"number": "1", "octave": 0, "duration": 1.0, "display_text": "1", "midi": 65, "note_name": "F4"},
                    {"number": "2", "octave": 0, "duration": 1.0, "display_text": "2", "midi": 67, "note_name": "G4"},
                    {"number": "3", "octave": 0, "duration": 1.0, "display_text": "3", "midi": 69, "note_name": "A4"}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 50, "note_name": "D3"},
                    {"number": "3", "octave": -2, "duration": 2.0, "display_text": "3̤", "midi": 45, "note_name": "A2"}
                ]
            },
            {
                "measureNumber": 14,
                "rightHand": [
                    {"number": "2", "octave": 0, "duration": 1.5, "display_text": "2", "midi": 67, "note_name": "G4"},
                    {"number": "1", "octave": 0, "duration": 0.5, "display_text": "1", "midi": 65, "note_name": "F4"},
                    {"number": "6", "octave": -1, "duration": 2.0, "display_text": "6̣", "midi": 62, "note_name": "D4"}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 2.0, "display_text": "4̤", "midi": 46, "note_name": "Bb2"},
                    {"number": "1", "octave": -2, "duration": 2.0, "display_text": "1̤", "midi": 41, "note_name": "F2"}
                ]
            },
            {
                "measureNumber": 15,
                "rightHand": [
                    {"number": "3", "octave": 0, "duration": 1.0, "display_text": "3", "midi": 69, "note_name": "A4"},
                    {"number": "5", "octave": 0, "duration": 1.0, "display_text": "5", "midi": 72, "note_name": "C5"},
                    {"number": "6", "octave": 0, "duration": 2.0, "display_text": "6", "midi": 74, "note_name": "D5"}
                ],
                "leftHand": [
                    {"number": "1", "octave": -1, "duration": 2.0, "display_text": "1̣", "midi": 53, "note_name": "F3"},
                    {"number": "5", "octave": -2, "duration": 2.0, "display_text": "5̤", "midi": 48, "note_name": "C3"}
                ]
            },
            {
                "measureNumber": 16,
                "rightHand": [
                    {"number": "6", "octave": 0, "duration": 1.5, "display_text": "6", "midi": 74, "note_name": "D5"},
                    {"number": "7", "octave": 0, "duration": 0.5, "display_text": "7", "midi": 76, "note_name": "E5"},
                    {"number": "1", "octave": 1, "duration": 1.0, "display_text": "1̇", "midi": 77, "note_name": "F5"},
                    {"number": "2", "octave": 1, "duration": 1.0, "display_text": "2̇", "midi": 79, "note_name": "G5"}
                ],
                "leftHand": [
                    {"number": "5", "octave": -2, "duration": 2.0, "display_text": "5̤", "midi": 48, "note_name": "C3"},
                    {"number": "2", "octave": -2, "duration": 2.0, "display_text": "2̤", "midi": 43, "note_name": "G2"}
                ]
            },
            {
                "measureNumber": 17,
                "rightHand": [
                    {"number": "3", "octave": 1, "duration": 2.0, "display_text": "3̇", "midi": 81, "note_name": "A5"},
                    {"number": "2", "octave": 1, "duration": 1.0, "display_text": "2̇", "midi": 79, "note_name": "G5"},
                    {"number": "1", "octave": 1, "duration": 1.0, "display_text": "1̇", "midi": 77, "note_name": "F5"}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 50, "note_name": "D3"},
                    {"number": "3", "octave": -2, "duration": 2.0, "display_text": "3̤", "midi": 45, "note_name": "A2"}
                ]
            },
            {
                "measureNumber": 18,
                "rightHand": [
                    {"number": "7", "octave": 0, "duration": 1.5, "display_text": "7", "midi": 76, "note_name": "E5"},
                    {"number": "1", "octave": 1, "duration": 0.5, "display_text": "1̇", "midi": 77, "note_name": "F5"},
                    {"number": "7", "octave": 0, "duration": 1.0, "display_text": "7", "midi": 76, "note_name": "E5"},
                    {"number": "5", "octave": 0, "duration": 1.0, "display_text": "5", "midi": 72, "note_name": "C5"}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 2.0, "display_text": "4̤", "midi": 46, "note_name": "Bb2"},
                    {"number": "1", "octave": -2, "duration": 2.0, "display_text": "1̤", "midi": 41, "note_name": "F2"}
                ]
            },
            {
                "measureNumber": 19,
                "rightHand": [
                    {"number": "6", "octave": 0, "duration": 2.0, "display_text": "6", "midi": 74, "note_name": "D5"},
                    {"number": "5", "octave": 0, "duration": 1.0, "display_text": "5", "midi": 72, "note_name": "C5"},
                    {"number": "3", "octave": 0, "duration": 1.0, "display_text": "3", "midi": 69, "note_name": "A4"}
                ],
                "leftHand": [
                    {"number": "1", "octave": -1, "duration": 2.0, "display_text": "1̣", "midi": 53, "note_name": "F3"},
                    {"number": "5", "octave": -2, "duration": 2.0, "display_text": "5̤", "midi": 48, "note_name": "C3"}
                ]
            },
            {
                "measureNumber": 20,
                "rightHand": [
                    {"number": "6", "octave": 0, "duration": 4.0, "display_text": "6", "midi": 74, "note_name": "D5"}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 4.0, "display_text": "6̤", "midi": 50, "note_name": "D3"}
                ]
            },
            {
                "measureNumber": 21,
                "rightHand": [
                    {"number": "3", "octave": 0, "duration": 2.0, "display_text": "3", "midi": 69, "note_name": "A4"},
                    {"number": "2", "octave": 0, "duration": 2.0, "display_text": "2", "midi": 67, "note_name": "G4"}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 4.0, "display_text": "6̤", "midi": 50, "note_name": "D3"}
                ]
            },
            {
                "measureNumber": 22,
                "rightHand": [
                    {"number": "1", "octave": 0, "duration": 2.0, "display_text": "1", "midi": 65, "note_name": "F4"},
                    {"number": "6", "octave": -1, "duration": 2.0, "display_text": "6̣", "midi": 62, "note_name": "D4"}
                ],
                "leftHand": [
                    {"number": "4", "octave": -2, "duration": 4.0, "display_text": "4̤", "midi": 46, "note_name": "Bb2"}
                ]
            },
            {
                "measureNumber": 23,
                "rightHand": [
                    {"number": "7", "octave": -1, "duration": 2.0, "display_text": "7̣", "midi": 64, "note_name": "E4"},
                    {"number": "5", "octave": -1, "duration": 2.0, "display_text": "5̣", "midi": 60, "note_name": "C4"}
                ],
                "leftHand": [
                    {"number": "5", "octave": -2, "duration": 4.0, "display_text": "5̤", "midi": 48, "note_name": "C3"}
                ]
            },
            {
                "measureNumber": 24,
                "rightHand": [
                    {"number": "6", "octave": -1, "duration": 4.0, "display_text": "6̣", "midi": 62, "note_name": "D4"}
                ],
                "leftHand": [
                    {"number": "6", "octave": -2, "duration": 4.0, "display_text": "6̤", "midi": 50, "note_name": "D3"}
                ]
            }
        ]
    }
}

def match_sample_song(query: str) -> Dict[str, Any] | None:
    """Matches user query or URL against known popular songs"""
    q = query.lower()
    if "victory" in q or "qySMrhVacQ8" in query:
        return SAMPLE_SONGS["victory"]
    for key, song in SAMPLE_SONGS.items():
        if key in q or song["title"].lower() in q or song["id"] in q:
            return song
        # Match youtube URL if present
        if song.get("youtubeSampleUrl") and song["youtubeSampleUrl"] in query:
            return song
    return None
