# 《FROM VICTORIA TO VICTORIA HARBOUR｜從維多利亞到維多利亞港》
## Seedance 2.5 Professional Production Prompt Suite (Pixar "UP" Style)

- **Film Title:** 《FROM VICTORIA TO VICTORIA HARBOUR｜從維多利亞到維多利亞港》
- **Source Story Excerpt:** `dog-v2.pdf` (The Shift End & Victoria Harbour Reunion)
- **Target Video Engine:** Seedance 2.5
- **Visual Style:** Pixar Feature Animation (*UP* Aesthetic — Pete Docter / Bob Peterson cinematic direction, warm 3D stylization, Dug-style canine fur & expressive soulful eyes)
- **Total Sequence Duration:** **56 Seconds**
- **Shot Duration Range:** **6s to 12s** (100% compliant with the 4s–30s parameter constraint)
- **Architecture Standard:** 100% compliant with the `library/` prompt template, semantic tags (`<<<element>>>`), closed diegetic audio lists, and strict positive/negative constraints.

---

## 1. Narrative Arc & Synopsis

Adapted directly from the climactic chapter of `dog-v2.pdf`, this animated sequence portrays the unforgettable twilight encounter between two Labrador Retriever brothers in Hong Kong:

1. **Shift's End:** Visually impaired owner Mr. Chen releases Tart's guide dog harness with an audible *Click*. Freed from the solemn duty of guiding human steps, Tart shakes off his working mindset and sits by the harbour.
2. **Parallel Path:** Tine finishes his community therapy visit and walks along the promenade with his handler, exploring curiously before suddenly freezing as an instinctual scent catches his nose.
3. **The Gaze:** Tart senses a familiar presence, slowly turning his golden head. Across the open promenade, the two dogs look at each other for the first time without working armor or service commands.
4. **The Approach:** Without reckless bounding or hesitation, they approach and share a sacred nose-to-nose sniff.
5. **Canine Resonance:** Tine's tail thumps the granite pavement twice. Tart responds with a soft, slow wag.
6. **The Handlers' Discovery:** The two handlers begin to chat. Discovering both dogs came from Australia, the word "Victoria" hangs in the air with electric amazement.
7. **The Pedigree Revelation:** Looking down at their official breeding records, they discover Tart and Tine not only hail from Victoria, Australia, but were born at the exact same pastoral dog farm. The two brothers rest side-by-side against the glowing skyline: **From Victoria to Victoria Harbour**.

---

## 2. Chronological Shot Schedule & Duration Breakdown

| Shot # | File Name | Scene Description | Shot Type | Duration | Aspect |
|---|---|---|---|:---:|:---:|
| **01** | [`001_shift-end-unharnessing-click.md`](001_shift-end-unharnessing-click.md) | Mr. Chen unclips Tart's harness (*Click*); whole-body dog shake & twilight release | Low-Angle Medium Close-Up | **8s** | 21:9 |
| **02** | [`002_tine-promenade-stroll-and-pause.md`](002_tine-promenade-stroll-and-pause.md) | Tine's relaxed evening stroll abruptly halted by instinctual scent recognition | Lateral Tracking to Locked Hold | **6s** | 21:9 |
| **03** | [`003_tart-senses-and-turns.md`](003_tart-senses-and-turns.md) | Tart senses the presence, turns his head over his shoulder; mutual locked gaze | Over-The-Shoulder Reverse Medium | **6s** | 21:9 |
| **04** | [`004_slow-approach-and-nose-sniff.md`](004_slow-approach-and-nose-sniff.md) | Reverent slow approach and intimate, quiet nose-to-nose greeting | Low Eye-Level Medium Two-Shot | **8s** | 21:9 |
| **05** | [`005_tail-thumping-and-response.md`](005_tail-thumping-and-response.md) | Tine thumps tail on granite (*thump... thump*); Tart responds with gentle wag | Low-Angle Medium Close-Up | **6s** | 21:9 |
| **06** | [`006_handlers-conversation-victoria.md`](006_handlers-conversation-victoria.md) | Handlers chat in Cantonese: "From Australia... Victoria?" and stunned realization | Eye-Level Medium Two-Shot | **10s** | 21:9 |
| **07** | [`007_pedigree-discovery-and-reunion.md`](007_pedigree-discovery-and-reunion.md) | Handlers trace identical dog farm on certificates; tilt up to brothers leaning together | Macro Tilt-Up to Hero Resolution | **12s** | 21:9 |
| **TOTAL** | **7 Continuous Shots** | **Complete Pixar "UP" Climactic Narrative Sequence** | **Full Cinematic Pipeline** | **56s** | **21:9** |

---

## 3. Production Asset Directory & Semantic Tagging

All reference assets have been consolidated and generated in authentic Pixar *UP* 3D animation style inside [`assets/dog-v2/`](../../assets/dog-v2/):

| Semantic Tag | Asset File Path | Type | Visual Characterization |
|---|---|---|---|
| `<<<char_tart_adult>>>` | [`assets/dog-v2/tart.png`](../../assets/dog-v2/tart.png) | Character (Dog) | Adult Golden Labrador Retriever in Pixar 3D *UP* style. Velvety honey-golden fur, soulful dark-amber eyes, black leather nose, disciplined athletic posture. (Turnaround reference). |
| `<<<char_tine_adult>>>` | [`assets/dog-v2/tine.png`](../../assets/dog-v2/tine.png) | Character (Dog) | Adult Chocolate Labrador Retriever in Pixar 3D *UP* style. Rich warm caramel-brown fur, distinct cream heart-shaped fur patch on right rear hip, warm hazel eyes, stocky broad chest. (Turnaround reference). |
| `<<<char_tart_owner>>>` | [`assets/dog-v2/char_tart_owner.png`](../../assets/dog-v2/char_tart_owner.png) | Character (Human) | Mr. Chen, visually impaired Hong Kong gentleman in Pixar 3D *UP* style (soft rounded features, stylish dark sunglasses, navy blue knit cardigan, cream shirt, white cane). Turnaround sheet. |
| `<<<char_tine_handler>>>` | [`assets/dog-v2/char_tine_handler.png`](../../assets/dog-v2/char_tine_handler.png) | Character (Human) | Young Hong Kong female community volunteer in Pixar 3D *UP* style (cheerful expressive face, short dark bob, turquoise volunteer vest, cream sweater, beige trousers). Turnaround sheet. |
| `<<<loc_tst_promenade_twilight>>>` | [`assets/dog-v2/loc_tst_promenade_twilight.png`](../../assets/dog-v2/loc_tst_promenade_twilight.png) | Environment | Tsim Sha Tsui waterfront promenade overlooking Victoria Harbour at twilight. Dark granite pavement, maritime iron railing, Victorian lampposts, and glowing Hong Kong Island skyline across the bay. |
| `<<<prop_pedigree_record>>>` | [`assets/dog-v2/prop_pedigree_record.png`](../../assets/dog-v2/prop_pedigree_record.png) | Prop | Open vintage leather folder on wooden promenade bench. Displays two official certificates: Tart and Tine both registered under "Victoria Valley Dog Farm, Victoria, Australia" with gold seals and blue paw stamps. |
| `<<<char_brothers_reunion>>>` | [`assets/dog-v2/char_brothers_reunion.png`](../../assets/dog-v2/char_brothers_reunion.png) | Character Hero | Climactic hero two-shot: Tart (Golden) and Tine (Chocolate with heart hip marking) sitting side-by-side at the promenade railing at night, leaning into each other with deep affection and peace. |

---

## 4. Prompt Architecture Standard Compliance

Every prompt file in this suite rigorously follows the 17-section standard established in [`library/TEMPLATE.md`](../../library/TEMPLATE.md):

1. **SCENE CONTEXT:** Concise dramatic logline and emotional point, written like a screenplay.
2. **OUTPUT SETTINGS:** Single continuous take, strict duration (6s to 12s), 21:9 aspect ratio, 1080p, real-time speed assertion.
3. **NO MUSIC — ABSOLUTE:** Exhaustive negative boilerplate prohibiting soundtrack music, synthetic strings, or melodramatic scores.
4. **ACTIVE REFERENCES:** Semantic tag bindings (`<<<element>>>`) specifying physical traits and ending with "100% matches the reference."
5. **LOCATION MAP / GEOGRAPHY:** Precise screen-space coordinates (screen-left, center, screen-right, camera height).
6. **FRAMING:** Precise shot scale, edge crops, headroom, and background diffusion.
7. **FIRST FRAME AND SPATIAL BLOCKING:** Exact definition of frame 0:00 to prevent establishing shot hallucinations.
8. **ACTION TIMING:** Second-by-second chronological beat breakdown ending on a held physical state.
9. **WHAT THIS SHOT IS DOING:** Subtext, psychological dynamics, and specific interpretations forbidden to the model.
10. **STYLE LOCK — PIXAR MOVIE "UP" AESTHETIC:** Feature 3D CGI animation standards, plush fur grooming, warm volumetric twilight lighting, Pete Docter staging.
11. **BREED & CANINE BEHAVIOR LOCK:** Labrador Retriever biomechanics, tail language, and mutual respect.
12. **PHYSICS:** Authentic canine mass, friction, inertia, cloth mechanics, and paw-ground contact.
13. **OPTICS:** Focal length equivalents (35mm to 75mm), aperture values, and depth of field consistency.
14. **CAMERA:** Exact support type (tripod, dolly slider, pedestal jib) and banned camera motions.
15. **LIGHTING:** Single motivated physical light source, directional quality, and forbidden lighting artifacts.
16. **AUDIO:** Closed, numbered diegetic sound lists.
17. **POSITIVE CONSTRAINTS:** Exhaustive invariant checklist.
