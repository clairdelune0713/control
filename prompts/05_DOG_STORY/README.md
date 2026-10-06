# 《SOMEWHERE BETWEEN US｜我們之間》
## Seedance 2.5 Professional Prompt Suite — Complete Production Package

- **Film Title:** 《SOMEWHERE BETWEEN US｜我們之間》 (*From Victoria to Victoria Harbour*)
- **Source Story:** `dog-story-20261006.md`
- **Target Video Model:** Seedance 2.5
- **Style Specification:** Classic Studio Ghibli Aesthetic (Hayao Miyazaki / Isao Takahata — *Kiki's Delivery Service*, *My Neighbor Totoro*, *Spirited Away*, *Whisper of the Heart*)
- **Total Film Duration:** **92 Seconds** (1 Minute 32 Seconds)
- **Individual Shot Durations:** 6s to 18s (all strictly compliant with the 4s–30s generation parameter)
- **Standard Compliance:** 100% compliant with the `library/` prompt architecture, section hierarchy, and negative constraints.

---

## 1. Executive Summary & Narrative Arc

Adapted from the Hong Kong Guide Dogs inspirational story (`dog-story-20261006.md`), this animated short film follows two Labrador Retriever littermate brothers: **Tart (蛋撻)**, a disciplined, steadfast guide dog representing Hong Kong's "Lion Rock Spirit" of silent devotion; and **Tine (阿華田 / Ovaltine)**, a warm, intuitive therapy dog representing Hong Kong's community warmth and empathy (*人情味*).

Separated in early puppyhood at Guide Dogs Victoria in Australia, they traverse parallel paths across the city of Hong Kong, repeatedly missing each other by mere seconds in the dense urban rush. Finally, after their work shifts end at twilight, their paths converge at Victoria Harbour, discovering they share not only the same heart, but the exact same origin: **From Victoria to Victoria Harbour**.

---

## 2. Chronological Shot Schedule & Duration Breakdown

| Shot # | File Name | Scene Description | Shot Type | Duration | Aspect |
|---|---|---|---|:---:|:---:|
| **01** | [`001_pastoral-dawn-victoria-australia.md`](001_pastoral-dawn-victoria-australia.md) | Dawn over the pastoral training hills of Victoria, Australia | Extreme Wide Landscape | **8s** | 21:9 |
| **02** | [`002_childhood-bond-puppies-in-meadow.md`](002_childhood-bond-puppies-in-meadow.md) | Baby Tart & Baby Tine tumbling in the clover meadow | Low-Angle Medium Close-Up | **10s** | 21:9 |
| **03** | [`003_match-cut-wind-to-victoria-harbour.md`](003_match-cut-wind-to-victoria-harbour.md) | Match-cut: wind in grass to Star Ferry waves in Victoria Harbour | Wide Seascape Pan | **6s** | 21:9 |
| **04** | [`004_tart-intelligent-disobedience-central.md`](004_tart-intelligent-disobedience-central.md) | Tart's intelligent disobedience saving handler in Central | Medium Street Action | **14s** | 21:9 |
| **05** | [`005_tine-quiet-presence-elderly-center.md`](005_tine-quiet-presence-elderly-center.md) | Tine quietly breaking through the loneliness of an isolated grandfather | Close-Medium Intimate Two-Shot | **16s** | 21:9 |
| **06** | [`006_near-miss-crossing-paths-star-ferry.md`](006_near-miss-crossing-paths-star-ferry.md) | Near-miss: crossing paths at Star Ferry Pier amid commuter crowd | Wide Moving Tracking Ensemble | **12s** | 21:9 |
| **07** | [`007_shift-end-unharnessing-tst-promenade.md`](007_shift-end-unharnessing-tst-promenade.md) | Shift's end: unharnessing Tart (*Click*) & whole-body dog shake | Medium Close-Up | **8s** | 21:9 |
| **08** | [`008_reunion-brothers-at-victoria-harbour.md`](008_reunion-brothers-at-victoria-harbour.md) | Climactic reunion of the two brothers against Victoria Harbour skyline | Medium-Wide Hero Resolution | **18s** | 21:9 |
| **TOTAL** | **8 Sequences** | **Complete Animated Short Film Arc** | **Full Cinematic Pipeline** | **92s** | **21:9** |

---

## 3. Production Asset Directory & Semantic Tagging

All reference assets have been generated in authentic Studio Ghibli gouache/watercolor aesthetic and archived in the workspace directory [`assets/dog_story/`](../../assets/dog_story/):

| Tag Name | Asset File | Category | Visual Specification |
|---|---|---|---|
| `<<<char_tart_adult>>>` | [`char_tart_adult.png`](../../assets/dog_story/char_tart_adult.png) | Character | Purebred Golden Labrador Retriever guide dog. Sleek athletic frame, golden honey coat, amber eyes, white HKGDA guide dog harness with rigid U-handle. Disciplined, calm, steadfast. |
| `<<<char_tine_adult>>>` | [`char_tine_adult.png`](../../assets/dog_story/char_tine_adult.png) | Character | Purebred Chocolate Labrador Retriever therapy dog. Stocky muscular build, rich mahogany chocolate coat, heart-shaped cowlick mark on rear hip, green therapy dog cape with paw patch. Cheerful, empathetic. |
| `<<<char_puppy_brothers>>>` | [`char_puppy_brothers.png`](../../assets/dog_story/char_puppy_brothers.png) | Character | 8-week-old Baby Tart (golden) and Baby Tine (chocolate with heart hip marking) playing together in sunlit green grass. |
| `<<<char_reunion_brothers>>>` | [`char_reunion_brothers.png`](../../assets/dog_story/char_reunion_brothers.png) | Character Hero | Adult Tart and Tine sitting side-by-side at Tsim Sha Tsui promenade railing at twilight, one golden, one chocolate, resting together. |
| `<<<loc_victoria_australia_farm>>>` | [`loc_victoria_australia_farm.png`](../../assets/dog_story/loc_victoria_australia_farm.png) | Environment | Guide Dogs Victoria campus in Australia. Rolling pastoral green hills, post-and-rail timber fences, eucalyptus trees, golden sunrise. |
| `<<<loc_hk_central_crossing>>>` | [`loc_hk_central_crossing.png`](../../assets/dog_story/loc_hk_central_crossing.png) | Environment | Central, Hong Kong. Green double-decker Ding Ding tram, zebra crossing, yellow tactile blister paving, bilingual signage, urban canyon. |
| `<<<loc_hk_community_center>>>` | [`loc_hk_community_center.png`](../../assets/dog_story/loc_hk_community_center.png) | Environment | Hong Kong elderly community day-care centre interior. Mint-green floor tiles, sunlit arched multi-pane windows, potted plants, quiet corner. |
| `<<<loc_victoria_harbour_twilight>>>` | [`loc_victoria_harbour_twilight.png`](../../assets/dog_story/loc_victoria_harbour_twilight.png) | Environment | Victoria Harbour at twilight from Tsim Sha Tsui promenade. Vintage green-and-white Star Ferry, gentle ripples, Hong Kong Island skyline glowing. |

---

## 4. Prompt Engineering Standard Compliance

Every prompt file adheres rigorously to the 17 core sections specified in [`library/TEMPLATE.md`](../../library/TEMPLATE.md):
1. **SCENE CONTEXT:** Concise dramatic logline and emotional point.
2. **OUTPUT SETTINGS:** Single continuous take, strict duration (6s to 18s), 21:9 format, real-time speed assertion.
3. **NO MUSIC — ABSOLUTE:** Exhaustive negative boilerplate barring synthetic pads, drums, or orchestral music beds.
4. **ACTIVE REFERENCES:** Semantic tag bindings (`<<<element>>>`) with physical descriptions and "100% matches reference".
5. **LOCATION MAP / GEOGRAPHY:** Explicit screen-space coordinates (screen-left, center, screen-right, camera height).
6. **FRAMING:** Precise shot scale, edge crops, headroom, and background diffusion.
7. **FIRST FRAME:** Exact definition of frame 0:00 to prevent establishing shot hallucinations.
8. **ACTION TIMING:** Second-by-second chronological beat breakdown ending on a held physical state.
9. **WHAT THIS SHOT IS DOING:** Subtext, psychological dynamics, and specific interpretations forbidden to the model.
10. **LOCK BLOCKS:** Domain-specific invariants:
    - `STYLE LOCK — STUDIO GHIBLI AESTHETIC` (hand-painted gouache, cel contours, zero sterile CGI).
    - `BREED & ANATOMY LOCK` (accurate Labrador Retriever biomechanics, weight, and fur behavior).
    - `CANINE EMOTIONAL & BEHAVIOR LOCK` (intelligent disobedience vs. gentle patience).
11. **PHYSICS:** Authentic canine mass, friction, inertia, cloth mechanics, and paw-ground contact.
12. **OPTICS:** Focal length equivalents (35mm, 50mm, 85mm), aperture values, and depth of field consistency.
13. **CAMERA:** Exact support type (tripod, dolly slider, shoulder rig) and banned camera motions.
14. **LIGHTING:** Single motivated physical light source, directional quality, and forbidden lighting artifacts.
15. **AUDIO:** Closed, numbered diegetic sound lists.
16. **POSITIVE CONSTRAINTS:** Exhaustive invariant checklist.
