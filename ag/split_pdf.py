#!/usr/bin/env python3
"""Split Reid.pdf into individual section PDFs based on menu.txt TOC."""

from pypdf import PdfReader, PdfWriter
import os

PDF_PATH = "/Users/shishengli/pairings-for-beginners/ag/Reid.pdf"
OUTPUT_DIR = "/Users/shishengli/pairings-for-beginners/ag/sections"

PAGE_OFFSET = 2  # PDF_page_1based = printed_page - PAGE_OFFSET

entries = []

# Chapter 0
entries.append((11, "ch00_woffle", "0 Woffle"))
entries.append((11, "ch00_s01_what_its_about", "0.1 What it's about"))
entries.append((12, "ch00_s02_specific_calculations_versus_general_theory", "0.2 Specific calculations vs general theory"))
entries.append((12, "ch00_s03_rings_of_functions_and_categories_of_geometry", "0.3 Rings of functions and categories"))
entries.append((13, "ch00_s04_geometry_from_polynomials", "0.4 Geometry from polynomials"))
entries.append((14, "ch00_s05_purely_algebraically_defined", "0.5 Purely algebraically defined"))
entries.append((14, "ch00_s06_plan_of_the_book", "0.6 Plan of the book"))
entries.append((15, "ch00_course_prerequisites", "Course prerequisites"))
entries.append((15, "ch00_course_relates_to", "Course relates to"))
entries.append((15, "ch00_exercises", "Exercises to Chapter 0"))
entries.append((16, "ch00_books", "Books"))

# Part I
entries.append((17, "part_I_playing_with_plane_curves", "Part I Playing with plane curves"))

# Chapter 1
entries.append((19, "ch01_plane_conics", "1 Plane conics"))
entries.append((19, "ch01_s01_example_of_a_parametrised_curve", "1.1 Example of a parametrised curve"))
entries.append((20, "ch01_s02_similar_example", "1.2 Similar example"))
entries.append((21, "ch01_s03_conics_in_r2", "1.3 Conics in R2"))
entries.append((21, "ch01_s04_projective_plane", "1.4 Projective plane"))
entries.append((23, "ch01_s05_equation_of_a_conic", "1.5 Equation of a conic"))
entries.append((23, "ch01_s05b_line_at_infinity_and_asymptotic_directions", "Line at infinity and asymptotic directions"))
entries.append((24, "ch01_s06_classification_of_conics_in_p2", "1.6 Classification of conics in P2"))
entries.append((25, "ch01_s07_parametrisation_of_a_conic", "1.7 Parametrisation of a conic"))
entries.append((25, "ch01_s08_homogeneous_form_in_2_variables", "1.8 Homogeneous form in 2 variables"))
entries.append((26, "ch01_s09_easy_cases_of_bezouts_theorem", "1.9 Easy cases of Bezout's Theorem"))
entries.append((27, "ch01_s10_corollary_unique_conic_through_5_general_points", "1.10 Corollary"))
entries.append((28, "ch01_s11_space_of_all_conics", "1.11 Space of all conics"))
entries.append((29, "ch01_s12_intersection_of_two_conics", "1.12 Intersection of two conics"))
entries.append((30, "ch01_s13_degenerate_conics_in_a_pencil", "1.13 Degenerate conics in a pencil"))
entries.append((30, "ch01_s14_worked_example", "1.14 Worked example"))
entries.append((32, "ch01_exercises", "Exercises to Chapter 1"))

# Chapter 2
entries.append((35, "ch02_cubics_and_the_group_law", "2 Cubics and the group law"))
entries.append((35, "ch02_s01_examples_of_parametrised_cubics", "2.1 Examples of parametrised cubics"))
entries.append((36, "ch02_s02_curve_has_no_rational_parametrisation", "2.2 No rational parametrisation"))
entries.append((37, "ch02_s03_lemma", "2.3 Lemma"))
entries.append((37, "ch02_s04_linear_systems", "2.4 Linear systems"))
entries.append((38, "ch02_s05_lemma_divisibility_by_l_or_by_q", "2.5 Lemma: divisibility"))
entries.append((39, "ch02_s06_proposition_cubics_through_8_general_points", "2.6 Proposition"))
entries.append((40, "ch02_s07_corollary_cubic_through_8_points", "2.7 Corollary"))
entries.append((40, "ch02_s08_group_law_on_a_plane_cubic", "2.8 Group law on a plane cubic"))
entries.append((42, "ch02_s09_associativity_in_general", "2.9 Associativity in general"))
entries.append((42, "ch02_s10_proof_by_continuity", "2.10 Proof by continuity"))
entries.append((43, "ch02_s11_pascals_theorem", "2.11 Pascal's Theorem"))
entries.append((44, "ch02_s12_inflexion_normal_form", "2.12 Inflexion, normal form"))
entries.append((45, "ch02_s13_simplified_group_law", "2.13 Simplified group law"))
entries.append((46, "ch02_exercises", "Exercises to Chapter 2"))
entries.append((49, "ch02_s14_topology_of_a_nonsingular_cubic", "2.14 Topology of a nonsingular cubic"))
entries.append((51, "ch02_s15_discussion_of_genus", "2.15 Discussion of genus"))
entries.append((51, "ch02_s16_commercial_break", "2.16 Commercial break"))

# Part II
entries.append((55, "part_II_the_category_of_affine_varieties", "Part II The category of affine varieties"))

# Chapter 3
entries.append((57, "ch03_affine_varieties_and_the_nullstellensatz", "3 Affine varieties and the Nullstellensatz"))
entries.append((57, "ch03_s01_definition_of_noetherian_ring", "3.1 Definition of Noetherian ring"))
entries.append((58, "ch03_s02_proposition_noetherian_passes_to_quotients", "3.2 Proposition"))
entries.append((58, "ch03_s03_hilbert_basis_theorem", "3.3 Hilbert Basis Theorem"))
entries.append((59, "ch03_s04_the_correspondence_v", "3.4 The correspondence V"))
entries.append((59, "ch03_s05_definition_the_zariski_topology", "3.5 The Zariski topology"))
entries.append((60, "ch03_s06_the_correspondence_i", "3.6 The correspondence I"))
entries.append((61, "ch03_s07_irreducible_algebraic_set", "3.7 Irreducible algebraic set"))
entries.append((62, "ch03_s08_preparation_for_the_nullstellensatz", "3.8 Preparation for Nullstellensatz"))
entries.append((62, "ch03_s09_definition_radical_ideal", "3.9 Radical ideal"))
entries.append((64, "ch03_s11_worked_examples", "3.11 Worked examples"))
entries.append((65, "ch03_s12_finite_algebras", "3.12 Finite algebras"))
entries.append((66, "ch03_s13_noether_normalisation", "3.13 Noether normalisation"))
entries.append((68, "ch03_s14_remarks", "3.14 Remarks"))
entries.append((68, "ch03_s15_proof_of_3_8", "3.15 Proof of (3.8)"))
entries.append((68, "ch03_s16_separable_addendum", "3.16 Separable addendum"))
entries.append((69, "ch03_s17_reduction_to_a_hypersurface", "3.17 Reduction to a hypersurface"))
entries.append((70, "ch03_exercises", "Exercises to Chapter 3"))

# Chapter 4
entries.append((73, "ch04_functions_on_varieties", "4 Functions on varieties"))
entries.append((73, "ch04_s01_polynomial_functions", "4.1 Polynomial functions"))
entries.append((73, "ch04_s02_kv_and_algebraic_subsets", "4.2 k[V] and algebraic subsets"))
entries.append((74, "ch04_s03_polynomial_maps", "4.3 Polynomial maps"))
entries.append((75, "ch04_s04_polynomial_maps_and_kv", "4.4 Polynomial maps and k[V]"))
entries.append((76, "ch04_s05_corollary_f_isomorphism", "4.5 Corollary"))
entries.append((77, "ch04_s06_affine_variety", "4.6 Affine variety"))
entries.append((77, "ch04_s07_function_field", "4.7 Function field"))
entries.append((78, "ch04_s08_criterion_for_dom_f", "4.8 Criterion for dom f"))
entries.append((78, "ch04_s09_rational_maps", "4.9 Rational maps"))
entries.append((79, "ch04_s10_composition_of_rational_maps", "4.10 Composition of rational maps"))
entries.append((79, "ch04_s11_theorem_dominant_rational_maps", "4.11 Theorem"))
entries.append((79, "ch04_s12_morphisms_from_open_subset", "4.12 Morphisms from open subset"))
entries.append((80, "ch04_s13_standard_open_subsets", "4.13 Standard open subsets"))
entries.append((81, "ch04_s14_worked_example", "4.14 Worked example"))
entries.append((82, "ch04_exercises", "Exercises to Chapter 4"))

# Part III
entries.append((85, "part_III_applications", "Part III Applications"))

# Chapter 5
entries.append((87, "ch05_projective_and_birational_geometry", "5 Projective and birational geometry"))
entries.append((87, "ch05_s00_why_projective_varieties", "5.0 Why projective varieties?"))
entries.append((88, "ch05_s01_graded_rings_and_homogeneous_ideals", "5.1 Graded rings"))
entries.append((89, "ch05_s02_the_homogeneous_vi_correspondences", "5.2 Homogeneous V-I correspondences"))
entries.append((89, "ch05_s03_projective_nullstellensatz", "5.3 Projective Nullstellensatz"))
entries.append((90, "ch05_s04_rational_functions_on_v", "5.4 Rational functions on V"))
entries.append((91, "ch05_s05_affine_covering", "5.5 Affine covering"))
entries.append((92, "ch05_s06_rational_maps_and_morphisms", "5.6 Rational maps and morphisms"))
entries.append((93, "ch05_s07_examples", "5.7 Examples"))
entries.append((94, "ch05_s08_birational_maps", "5.8 Birational maps"))
entries.append((95, "ch05_s09_rational_varieties", "5.9 Rational varieties"))
entries.append((95, "ch05_s10_reduction_to_a_hypersurface", "5.10 Reduction to a hypersurface"))
entries.append((95, "ch05_s11_products", "5.11 Products"))
entries.append((96, "ch05_exercises", "Exercises to Chapter 5"))

# Chapter 6
entries.append((101, "ch06_tangent_space_and_nonsingularity_dimension", "6 Tangent space and nonsingularity"))
entries.append((101, "ch06_s01_nonsingular_points_of_a_hypersurface", "6.1 Nonsingular points"))
entries.append((102, "ch06_s02_remarks", "6.2 Remarks"))
entries.append((102, "ch06_s03_proposition_v_nonsing_is_dense", "6.3 V nonsing is dense"))
entries.append((103, "ch06_s04_tangent_space", "6.4 Tangent space"))
entries.append((103, "ch06_s05_proposition_dim_tp_v_upper_semicontinuous", "6.5 dim TP V upper semicontinuous"))
entries.append((103, "ch06_s06_corollary_definition_dim_tp_v", "6.6 Corollary-Definition"))
entries.append((104, "ch06_s07_dim_v_tr_deg_hypersurface_case", "6.7 dim V = tr deg"))
entries.append((104, "ch06_s08_intrinsic_nature_of_tp_v", "6.8 Intrinsic nature of TP V"))
entries.append((105, "ch06_s09_corollary_tp_v_depends_on_p", "6.9 Corollary"))
entries.append((106, "ch06_s10_theorem_dim_v_tr_deg", "6.10 Theorem"))
entries.append((106, "ch06_s11_nonsingularity_and_projective_varieties", "6.11 Nonsingularity and projective"))
entries.append((106, "ch06_s12_worked_example_blowup", "6.12 Worked example: blowup"))
entries.append((107, "ch06_exercises", "Exercises to Chapter 6"))

# Chapter 7
entries.append((109, "ch07_the_27_lines_on_a_cubic_surface", "7 The 27 lines"))
entries.append((109, "ch07_s01_consequences_of_nonsingularity", "7.1 Consequences of nonsingularity"))
entries.append((110, "ch07_s02_proposition_existence_of_a_line", "7.2 Existence of a line"))
entries.append((112, "ch07_s03_proposition_lines_meeting_a_given_line", "7.3 Lines meeting a given line"))
entries.append((114, "ch07_s04_corollary_two_disjoint_lines", "7.4 Two disjoint lines"))
entries.append((114, "ch07_s05_finding_all_the_lines", "7.5 Finding all the lines"))
entries.append((115, "ch07_s06_the_27_lines", "7.6 The 27 lines"))
entries.append((116, "ch07_s07_the_configuration_of_lines", "7.7 Configuration of lines"))
entries.append((117, "ch07_exercises", "Exercises to Chapter 7"))

# Chapter 8
entries.append((121, "ch08_final_comments", "8 Final comments"))
entries.append((121, "ch08_s01_introduction", "8.1 Introduction"))
entries.append((121, "ch08_s02_prehistory", "8.2 Prehistory"))
entries.append((122, "ch08_s03_rigour_the_first_wave", "8.3 Rigour, the first wave"))
entries.append((122, "ch08_s04_the_grothendieck_era", "8.4 The Grothendieck era"))
entries.append((123, "ch08_s05_the_big_bang", "8.5 The big bang"))
entries.append((124, "ch08_s06_choice_of_topics", "8.6 Choice of topics"))
entries.append((124, "ch08_s07_computation_versus_theory", "8.7 Computation versus theory"))
entries.append((124, "ch08_s08_r_versus_c", "8.8 R versus C"))
entries.append((125, "ch08_s09_regular_functions_and_sheaves", "8.9 Regular functions and sheaves"))
entries.append((125, "ch08_s10_globally_defined_regular_functions", "8.10 Globally defined regular functions"))
entries.append((125, "ch08_s11_surprising_sufficiency_of_projective_ag", "8.11 Surprising sufficiency"))
entries.append((126, "ch08_s12_affine_varieties_and_schemes", "8.12 Affine varieties and schemes"))
entries.append((127, "ch08_s13_whats_the_point", "8.13 What's the point?"))
entries.append((129, "ch08_s14_how_schemes_are_more_general", "8.14 How schemes are more general"))
entries.append((131, "ch08_s15_proof_existence_of_lines_on_cubic_surface", "8.15 Proof of existence of lines"))
entries.append((132, "ch08_s16_acknowledgements_and_name_dropping", "8.16 Acknowledgements"))

print(f"Total TOC entries: {len(entries)}")

# Load PDF
reader = PdfReader(PDF_PATH)
total_pdf_pages = len(reader.pages)
print(f"Total PDF pages: {total_pdf_pages}")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for i, (printed_page, filename, description) in enumerate(entries):
    # Start PDF page (0-indexed)
    start_pdf_0 = printed_page - PAGE_OFFSET - 1

    # End PDF page: include up to next section's start page (inclusive)
    if i + 1 < len(entries):
        next_printed_page = entries[i + 1][0]
        end_pdf_0 = next_printed_page - PAGE_OFFSET - 1  # next section's start page (0-indexed)
    else:
        end_pdf_0 = total_pdf_pages - 1

    start_pdf_0 = max(0, start_pdf_0)
    end_pdf_0 = min(total_pdf_pages - 1, end_pdf_0)

    if start_pdf_0 > end_pdf_0:
        print(f"  SKIP (invalid range): {filename}")
        continue

    writer = PdfWriter()
    for p in range(start_pdf_0, end_pdf_0 + 1):
        writer.add_page(reader.pages[p])

    out_path = os.path.join(OUTPUT_DIR, filename + ".pdf")
    with open(out_path, "wb") as f:
        writer.write(f)

    num_pages = end_pdf_0 - start_pdf_0 + 1
    print(f"  [{i+1:3d}/{len(entries)}] {filename}.pdf  (printed p.{printed_page}, PDF p.{start_pdf_0+1}-{end_pdf_0+1}, {num_pages} pg) - {description}")

print(f"\nDone! Files written to {OUTPUT_DIR}")
