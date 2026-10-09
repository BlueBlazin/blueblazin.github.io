"""Source-backed Kernel Zoo catalogue. Examples and explanatory diagrams are original."""
FAMILIES = [
 ("physical", "Physical cores", "A seed, an inner part, or a starting region.", "#a15a15", "core", ["grain", "nut", "atom", "flame", "fuel"]),
 ("zero", "What a map collapses", "Inputs sent to zero, or inputs a map identifies.", "#315ad5", "null", ["nullspace", "homomorphism", "congruence", "isogeny"]),
 ("influence", "Weights & influences", "A function or neighborhood that describes an operation.", "#087b70", "wave", ["convolution", "CNN", "PDE", "probability", "physics"]),
 ("similarity", "Inner products & similarity", "Pairwise functions with additional mathematical structure.", "#8050a7", "gram", ["SVM", "RKHS", "Gaussian process", "NTK"]),
 ("subset", "Distinguished subsets", "A region or subset picked out by a defining property.", "#b43f53", "region", ["visibility", "graph", "viability", "topology"]),
 ("compute", "Executable computations", "A routine that performs a computational operation.", "#0073a6", "grid", ["CUDA", "Metal", "Triton", "Pallas", "BLAS"]),
 ("engine", "Core engines", "The central machinery of a software system.", "#5b6580", "layers", ["Linux", "Lean", "Jupyter", "CAD", "simulation"]),
 ("reduction", "Reduced problems", "A smaller instance with a formal preservation guarantee.", "#647626", "reduce", ["kernelization", "parameterized complexity"]),
 ("space", "Spacecraft data", "A SPICE file containing mission geometry or supporting data.", "#9556b2", "orbit", ["ephemeris", "attitude", "frames", "time"]),
]
SOURCES = {}
def S(key,title,url,publisher,kind="Documentation"):
    SOURCES[key] = dict(title=title,url=url,publisher=publisher,kind=kind)

S("grain","Corn processing and kernel composition","https://www.extension.purdue.edu/extmedia/id/id-333.pdf","Purdue Extension","University publication")
S("nut","Growing walnuts in Oregon","https://extension.oregonstate.edu/catalog/pub/em-8907-growing-walnuts-oregon","Oregon State University","University publication")
S("lewis","The Atom and the Molecule (1916)","https://gskim071031.github.io/Pages/Classic-Papers/Lewis-1916/","G. N. Lewis; JACS (historical paper transcription)","Original paper")
S("flame","Analysis on ignition kernel formation in a quiescent mixture","https://www.sciencedirect.com/science/article/pii/S0010218022003510","Combustion and Flame","Research paper")
S("fuel","TRISO Particles","https://www.energy.gov/ne/photos/triso-particles","U.S. Department of Energy","Institutional reference")
S("linear","Linear Algebra: kernels of matrices","https://math.mit.edu/~tangkai/note/rec23F/1003.pdf","MIT Mathematics","Lecture notes")
S("group","Homomorphisms and Isomorphisms","https://pi.math.cornell.edu/~mec/2008-2009/Victor/part6.htm","Cornell Mathematics","Lecture notes")
S("ring","Commutative Algebra","https://pi.math.cornell.edu/~zbnorwood/partiii/files/commalgnotes.pdf","Zachary Norwood / Cornell","Lecture notes")
S("module","Universal property of kernels and cokernels","https://math.stanford.edu/~church/teaching/210A-F17/math210A-F17-hw2-sols.pdf","Stanford Mathematics","Course solutions")
S("operator","Laplace equation and the kernel of a differential operator","https://people.math.harvard.edu/~knill/teaching/math21b2003/laplace/index.html","Oliver Knill / Harvard","Lecture notes")
S("congruence","The Kernel of a Homomorphism","https://voutsadakis.com/TEACH/LECTURES/UNVALG/Chapter2a.pdf","George Voutsadakis","Lecture notes")
S("category","Generalities on Abelian Categories","https://www.math.mcgill.ca/barr/papers/gk.pdf","Grothendieck; hosted by Michael Barr","Mathematical text")
S("pair","Cartan–Eilenberg Cohomology and Triples","https://www.math.mcgill.ca/barr/ftp/pdffiles/coho.pdf","Michael Barr","Research paper")
S("isogeny","Elliptic Curves: isogenies from kernels","https://math.mit.edu/classes/18.783/2019/LectureNotes6.pdf","Andrew Sutherland / MIT","Lecture notes")
S("code","Generic structures for linear codes","https://doc.sagemath.org/html/en/reference/coding/sage/coding/linear_code.html","SageMath")
S("schwartz","The basics of microlocal analysis","https://math.stanford.edu/~andras/grenoble-psdo.pdf","András Vasy / Stanford","Lecture notes")
S("convolve","Multidimensional convolution","https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.convolve.html","SciPy")
S("cnn","Conv2d","https://docs.pytorch.org/docs/2.14/generated/torch.nn.Conv2d.html","PyTorch")
S("morph","Image Filtering: morphology","https://docs.opencv.org/4.5.4/d4/d86/group__imgproc__filter.html","OpenCV")
S("transform","The Fourier Transform and Laplace Transform","https://people.math.harvard.edu/~shlomo/212a/06.pdf","Shlomo Sternberg / Harvard","Lecture notes")
S("green","Differential Analysis: fundamental solutions","https://ocw.mit.edu/courses/18-156-differential-analysis-spring-2004/62906408ea3a1fde43dee67b2c5ee0d0_lec0.pdf","MIT OpenCourseWare","Lecture notes")
S("heat","The Fundamental Solution for the Heat Equation","https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2011/9acdeff6449529106ac254f7ada967da_MIT18_152F11_lec_05.pdf","Jared Speck / MIT","Lecture notes")
S("poisson","PDE notes: Poisson kernel","https://math.stanford.edu/~ryzhik/STANFORD/STANF272-15/notes-272-15.pdf","Lenya Ryzhik / Stanford","Lecture notes")
S("fourier","Fejér's Theorem and Convergence of Fourier Series","https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/resources/18102-sp21-lecture-16/","MIT OpenCourseWare","Lecture")
S("mollify","Approximate identities and Fourier analysis","https://math.uchicago.edu/~may/REU2017/REUPapers/Zhang%2CLingxian.pdf","Lingxian Zhang / University of Chicago","Mathematical exposition")
S("singular","Singular kernels and Calderón–Zygmund operators","https://math.jhu.edu/~lindblad/633/notes4.pdf","Terence Tao; hosted at Johns Hopkins","Lecture notes")
S("hilbert","A Short Tour of Harmonic Analysis","https://math.uchicago.edu/~may/REU2013/REUPapers/Talbut.pdf","Beatrice Talbut / University of Chicago","Mathematical exposition")
S("cauchy","Complex Variables: Cauchy's integral formula","https://math.mit.edu/~dunkel/Teach/18.04_2019S/notes/1804_Main.pdf","MIT Mathematics","Lecture notes")
S("kde","Kernel density estimation","https://docs.scipy.org/doc/scipy-1.14.0/tutorial/stats/kernel_density_estimation.html","SciPy")
S("regression","KernelReg: nonparametric kernel regression","https://www.statsmodels.org/dev/generated/statsmodels.nonparametric.kernel_regression.KernelReg.html","statsmodels")
S("reconstruct","Images and image filtering: resampling","https://www.cs.cornell.edu/courses/cs4670/2013fa/lectures/lec03_resample.pdf","Cornell Computer Science","Lecture notes")
S("probability","Transition kernels and completely positive maps","https://people.math.ethz.ch/~sibecker/steffens.pdf","ETH Zürich","Seminar notes")
S("markov","Markov Chains: Definitions","https://www.math.ucla.edu/~biskup/275c.1.25s/PDFs/ch29.pdf","Marek Biskup / UCLA","Lecture notes")
S("likelihood","Proportionality Constants","https://mc-stan.org/docs/2_34/stan-users-guide/proportionality-constants.html","Stan")
S("steinprob","Stein kernels and moment maps","https://www.normalesup.org/~mfathi/docs/Stein%20kernels%20and%20OT%2C%20revised%20version.pdf","Max Fathi","Research paper")
S("volterra","Nonlinear System Analysis Based on the Volterra Series","https://pure.southwales.ac.uk/files/2109606/M._Weiss_2003_2059431.pdf","M. Weiss / University of South Wales","Thesis")
S("memory","Microscopic theory of Brownian motion: Mori friction kernel","https://www.sciencedirect.com/science/article/pii/0378437175901624","Physica A","Research paper")
S("dispersal","When will plant morphology affect the shape of a seed dispersal kernel?","https://pubmed.ncbi.nlm.nih.gov/11444954/","Ecology / PubMed","Research paper")
S("collision","Well-posedness of Smoluchowski's coagulation equation","https://doi.org/10.1016/j.jfa.2005.07.013","N. Fournier and P. Laurençot","Research paper")
S("sensitivity","Three-dimensional waveform sensitivity kernels","https://pure.amsterdamumc.nl/en/publications/three-dimensional-waveform-sensitivity-kernels/","Research authors / institutional repository","Research paper")
S("averaging","Intercomparison of remote sounding instruments","https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2002JD002299","C. D. Rodgers and B. J. Connor","Research paper")
S("shield","Point-Kernel Code Development for Gamma-Ray Shielding Applications","https://www.mdpi.com/2076-3417/15/14/7795","Applied Sciences","Research paper")
S("xc","Hamiltonian and exchange–correlation response","https://www.octopus-code.org/documentation/14/manual/basics/hamiltonian/","Octopus")
S("bethe","Interaction kernel in the Bethe–Salpeter equation","https://arxiv.org/abs/hep-th/0202026","Jun-Chen Su","Research paper")
S("kpm","The Kernel Polynomial Method","https://arxiv.org/abs/cond-mat/0504627","Weiße, Wellein, Alvermann and Fehske","Research review")
S("rkhs","Reproducing kernel Hilbert spaces","https://web.stanford.edu/class/stats305c/lectures/RKHS.html","Stanford Statistics","Lecture notes")
S("svm","Kernels and support vector machines","https://web.stanford.edu/class/stats202/notes/Support-vector-machines/Kernels.html","Stanford Statistics","Lecture notes")
S("gp","Gaussian Processes for Machine Learning: covariance functions","https://gaussianprocess.org/gpml/chapters/RW4.pdf","Rasmussen and Williams / MIT Press","Author-hosted book")
S("pairwise","Pairwise kernel functions","https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.pairwise_kernels.html","scikit-learn")
S("ntk","Neural Tangent Kernel: Convergence and Generalization","https://arxiv.org/abs/1806.07572","Jacot, Gabriel and Hongler","Research paper")
S("graphml","Graph Kernels","https://www.jmlr.org/papers/volume11/vishwanathan10a/vishwanathan10a.pdf","Vishwanathan et al. / JMLR","Research paper")
S("string","Fast String Kernels","https://www.jmlr.org/papers/volume5/leslie04a/leslie04a.pdf","Leslie and Kuang / JMLR","Research paper")
S("fisher","Exploiting Generative Models in Discriminative Classifiers","https://papers.nips.cc/paper_files/paper/1998/hash/db1915052d15f7815c8b88e879465a1e-Abstract.html","Jaakkola and Haussler / NeurIPS","Research paper")
S("mmd","A Kernel Two-Sample Test","https://www.jmlr.org/papers/v13/gretton12a.html","Gretton et al. / JMLR","Research paper")
S("steinml","A Kernelized Stein Discrepancy for Goodness-of-fit Tests","https://proceedings.mlr.press/v48/liub16.html","Liu, Lee and Jordan / ICML","Research paper")
S("quantum","Supervised learning with quantum enhanced feature spaces","https://arxiv.org/abs/1804.11326","Havlíček et al.","Research paper")
S("bergman","Functional analysis: Bergman projection","https://math.berkeley.edu/~moorxu/oldsite/notes/205b/205bmain.pdf","UC Berkeley","Lecture notes")
S("szego","A Szegő Kernel for Discrete Series","https://www.math.stonybrook.edu/~aknapp/pdf-files/proc-icm-szego-1974.pdf","Anthony Knapp / ICM","Research paper")
S("dpp","Random point fields and random matrices","https://www.cambridge.org/core/books/abs/random-matrices-high-dimensional-phenomena/random-point-fields-and-random-matrices/3ABEF2AA9A747C36EA24E51CDFE23EE8","Gordon Blower / Cambridge University Press","Author's book chapter")
S("digraph","Combinatorial Game Theory Foundations Applied to Digraph Kernels","https://www.combinatorics.org/ojs/index.php/eljc/article/view/v4i2r10","Aviezri Fraenkel / Electronic Journal of Combinatorics","Research paper")
S("polygon","Computational Geometry: An Introduction","https://www.cs.rpi.edu/~cutler/classes/computationalgeometry/F23/references/Computational_Geometry_An_Introduction.pdf","Preparata and Shamos; RPI-hosted text","Mathematical textbook")
S("viability","A Survey of Viability Theory","https://epubs.siam.org/doi/abs/10.1137/0328044","Jean-Pierre Aubin / SIAM","Research paper")
S("discriminate","The calculation of discriminating kernel","https://link.springer.com/article/10.1186/s13662-017-1429-2","Advances in Continuous and Discrete Models","Research paper")
S("perfect","Descriptive Set Theory: Cantor–Bendixson","https://www.math.mcgill.ca/atserunyan/Teaching_notes/dst_lectures.pdf","Anush Tserunyan","Lecture notes")
S("saturation","Λrs-open sets and Λrs-closed sets in topological spaces","https://www.scik.org/index.php/jmcs/article/view/6687","Amutha and Dhana Balan","Research paper")
S("semigroup","Semigroup kernels: dissertation text","https://people.cs.uchicago.edu/~laci/students/toumpakari-phd.pdf","E. Toumpakari / University of Chicago","Thesis")
S("radical","Product of distinct prime factors of n","https://oeis.org/wiki/Product_of_distinct_prime_factors_of_n","OEIS Foundation","Mathematical reference")
S("belief","Kernel contraction","https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/kernel-contraction/C822638049E45B34EE10FBE45A8865E1","Sven Ove Hansson / Journal of Symbolic Logic","Research paper")
S("games","The kernel of a cooperative game","https://onlinelibrary.wiley.com/doi/10.1002/nav.3800120303","Morton Davis and Michael Maschler","Original paper")
S("ks","Kernel Search: An application to the index tracking problem","https://www.sciencedirect.com/science/article/pii/S0377221711008071","European Journal of Operational Research","Research paper")
S("kern","On the kern of a general cross section","https://www.sciencedirect.com/science/article/pii/S0020768398003370","Massood Mofid and Arash Yavari","Research paper")
S("cuda","Writing SIMT Kernels","https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html","NVIDIA")
S("opencl","Qualifiers for Kernel Functions","https://registry.khronos.org/OpenCL/specs/unified/refpages/man/html/kernel.html","Khronos Group","Specification")
S("metal","Metal library function entry points","https://developer.apple.com/documentation/metal/mtllibrary/functionnames","Apple")
S("hip","Introduction to the HIP programming model","https://rocm.docs.amd.com/projects/HIP/en/develop/understand/programming_model.html","AMD")
S("shader","Compute Shaders","https://docs.vulkan.org/guide/latest/compute_shaders.html","Khronos Group")
S("triton","Vector Addition","https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html","Triton")
S("pallas","Pallas Quickstart","https://docs.jax.dev/en/latest/pallas/quickstart.html","JAX")
S("blas","Anatomy of High-Performance Many-Threaded Matrix Multiplication","https://www.cs.utexas.edu/~flame/pubs/blis3_ipdps14.pdf","Smith, van de Geijn et al. / UT Austin","Research paper")
S("dispatch","Registering a Dispatched Operator in C++","https://docs.pytorch.org/tutorials/advanced/dispatcher","PyTorch")
S("tf","Create an op","https://www.tensorflow.org/guide/create_op","TensorFlow")
S("fusion","XLA:GPU Architecture Overview","https://openxla.org/xla/gpu_architecture","OpenXLA")
S("linux","The Linux Kernel documentation","https://docs.kernel.org/","Linux kernel community")
S("sel4","The seL4 Microkernel: An Introduction","https://sel4.systems/About/whitepaper.html","seL4 Foundation")
S("exo","Exokernel: application-level resource management","https://www.cs.cornell.edu/courses/cs614/1999sp/notes98/exokernel.html","Engler, Kaashoek and O'Toole; Cornell course notes","Paper discussion")
S("security","Security kernel","https://csrc.nist.gov/glossary/term/security_kernel","NIST CSRC","Standards terminology")
S("lean","Elaboration and Compilation: the kernel","https://lean-lang.org/doc/reference/latest/Elaboration-and-Compilation/","Lean")
S("lcf","Publications on LCF and HOL","https://www.cl.cam.ac.uk/~lp15/papers/hol.html","Lawrence Paulson / Cambridge","Author's explanation")
S("jupyter","Kernels (Programming Languages)","https://docs.jupyter.org/en/stable/projects/kernels.html","Project Jupyter")
S("wolfram","The Wolfram front end and kernel","https://reference.wolfram.com/language/ref/%24FrontEnd.html.en","Wolfram Research")
S("cgal","2D and 3D Geometry Kernel","https://doc.cgal.org/Manual/3.5/doc_html/cgal_manual/Kernel_23/Chapter_main.html","CGAL")
S("cad","Parasolid 3D Geometric Modeling","https://www.siemens.com/en-us/products/plm-components/parasolid/","Siemens")
S("systemc","SystemC and Transaction-Level Modeling","https://systemc.org/overview/systemc-tlm/","Accellera / SystemC")
S("kernelization","What is known about Vertex Cover Kernelization?","https://arxiv.org/abs/1811.09429","Fellows, Jaffke, Király, Rosamond and Weller","Research survey")
S("spice","Introduction to SPICE","https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/info/intrdctn.html","NASA / JPL NAIF")
S("spicefiles","SPICE Kernel Required Reading","https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/kernel.html","NASA / JPL NAIF")
S("spk","SPK Required Reading","https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/spk.html","NASA / JPL NAIF")
S("ck","C-Kernel Required Reading","https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/ck.html","NASA / JPL NAIF")
S("pck","PCK Required Reading","https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/pck.html","NASA / JPL NAIF")
S("dsk","DSK Required Reading","https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/dsk.html","NASA / JPL NAIF")
S("lie","Introduction to Lie Algebras: homomorphisms","https://math.mit.edu/classes/18.745/Notes/Lecture_2_Notes.pdf","MIT Mathematics","Lecture notes")
S("poissondisk","The Poisson kernel on the unit disc","https://www.cmi.ac.in/~pramath/GradComplex_2017/Lectures/Lecture20.pdf","Chennai Mathematical Institute","Lecture notes")
S("attention","Transformers are RNNs: Linear Attention","https://arxiv.org/abs/2006.16236","Katharopoulos, Vyas, Pappas and Fleuret","Research paper")
S("sph","Smoothed Particle Hydrodynamics","https://arxiv.org/abs/1007.1245","Peter J. Cossins","Research review")
S("path","Basic analytic combinatorics of directed lattice paths","https://lipn.fr/~banderier/Papers/tcs_banderier_flajolet_2002.pdf","Cyril Banderier and Philippe Flajolet","Research paper")
S("lossy","Lossy Kernelization","https://arxiv.org/abs/1604.04111","Lokshtanov, Panolan, Ramanujan and Saurabh","Research paper")

ENTRIES = []
def E(id,family,name,domain,short,body,tex,example,note,refs,related=(),visual=None,variants=(),code=None,status="Meaning"):
    ENTRIES.append(dict(id=id,family=family,name=name,domain=domain,short=short,body=body,tex=tex,example=example,note=note,refs=refs.split(),related=list(related),visual=visual or dict((f[0],f[4]) for f in FAMILIES)[family],variants=list(variants),code=code,status=status))

# Physical objects and regions.
E("grain","physical","Grain kernel","Botany · agriculture","The grain itself, including its seed tissues.",
  "In cereals, a kernel is a grain: botanically a caryopsis, a fruit whose wall is closely joined to the seed coat. A corn kernel contains protective outer tissues, endosperm and an embryo (germ).",
  "", "A maize kernel contains a developing plant and stored food. Milling separates useful fractions such as germ, starch and fiber.",
  "A corn kernel is not just the germ. Likewise, an acorn is a whole nut; its inner seed can be called its kernel.", "grain", ["nut"],variants=["Corn / maize","Wheat","Rice","Other cereal grains"])
E("nut","physical","Nut kernel","Botany · food science","The seed or edible inner part inside a shell.",
  "In nut processing, kernel names the inner seed material recovered when the shell is removed. Everyday culinary categories need not match botanical categories.",
  "", "Crack a walnut: the lobed seed inside is the walnut kernel. Kernel color, shriveling and recovery yield are quality measurements.",
  "An almond is botanically the seed of a drupe; the culinary label nut does not change what processors mean by kernel.", "nut", ["grain"])
E("atomic","physical","Atomic kernel","Historical chemistry","An atom's inner core, excluding its outer electrons.",
  "Lewis's 1916 account distinguishes an inner kernel from an outer electron shell. In this terminology, the kernel comprises the nucleus and inner electrons; valence electrons lie outside it.",
  "\\text{atomic kernel}=\\text{nucleus}+\\text{core electrons}", "For carbon in a simple shell picture, the nucleus and two inner electrons form a core with net charge +4; four valence electrons sit outside.",
  "This is historical chemical language. Kernel is not the usual modern name for an atomic nucleus, and Lewis's original atom model is not modern quantum mechanics.", "lewis", ["fuel"],status="Historical usage")
E("flame","physical","Flame / ignition kernel","Combustion","A small ignition region that may grow into a flame.",
  "A localized heated or reacting region initiates combustion. A successful ignition kernel develops into a self-sustaining flame; a weak one can be extinguished by heat loss or stretching.",
  "", "A spark in an engine creates a small hot region. Whether that region survives and grows helps determine whether ignition succeeds.",
  "Here kernel is a physical region, not a numerical filter used to simulate combustion.", "flame", ["heat","collision"],visual="pulse")
E("fuel","physical","Nuclear fuel kernel","Nuclear engineering · materials","The fuel-bearing core of a coated particle.",
  "A TRISO particle encloses a small fuel kernel, commonly uranium dioxide or uranium oxycarbide, within protective carbon and silicon-carbide layers.",
  "\\text{fuel kernel}\\subset\\text{coated TRISO particle}", "In a coated fuel particle, fission occurs in the fuel-bearing core; the surrounding layers retain fission products and protect the core.",
  "This is a material component. A radiation point kernel is instead a mathematical response function.", "fuel", ["shield"],visual="core")

# A map's zero fiber and its categorical or relational generalizations.
E("nullspace","zero","Linear-algebra kernel","Linear algebra","Every vector a linear map sends to zero.",
  "The kernel, or nullspace, of a linear map A is the subspace of inputs x satisfying Ax = 0. It records directions that the map loses.",
  "\\ker A=\\{x:Ax=0\\}", "For A = [1  2], every vector t(−2, 1) maps to zero. The kernel is a line, not the zero vector alone.",
  "A matrix used as an image filter is also called a kernel, but its nullspace is a different object.", "linear", ["operator","code","integral"],visual="null")
E("group","zero","Group-homomorphism kernel","Abstract algebra","Group elements sent to the identity.",
  "For a group homomorphism φ, the kernel is the preimage of the target group's identity. It is a normal subgroup; quotienting by it removes exactly the distinctions that φ loses.",
  "\\ker\\varphi=\\{g\\in G:\\varphi(g)=e_H\\}", "Reduction modulo 3 maps the additive group of integers to ℤ/3ℤ. Its kernel is 3ℤ.",
  "Zero is the identity for additive groups. For multiplicative groups, use the identity 1 instead.", "group", ["ring","congruence","isogeny"],visual="map")
E("ring","zero","Ring-homomorphism kernel","Commutative algebra","Ring elements sent to zero; an ideal.",
  "The zero fiber of a ring homomorphism is an ideal. In algebraic geometry, such kernels can encode equations imposed by a map of coordinate rings.",
  "\\ker\\varphi=\\varphi^{-1}(0)", "Evaluation at 2 sends a polynomial p(x) to p(2). Over ℝ[x], its kernel is the ideal generated by x−2.",
  "In the category of unital rings, the zero map is generally not a unital morphism. The ideal kernel and the categorical zero-map construction need care.", "ring", ["module","category","group"],visual="map")
E("module","zero","Module / Lie-algebra kernel","Algebra","A submodule or ideal consisting of zero-mapped elements.",
  "A module homomorphism's zero fiber is a submodule. A Lie-algebra homomorphism's zero fiber is a Lie ideal. These are algebraic versions of the same map-to-zero idea.",
  "\\ker f=\\{m:f(m)=0\\}", "The homomorphism ℤ → ℤ/4ℤ has kernel 4ℤ, viewed as a ℤ-submodule of ℤ.",
  "Different ambient algebraic structures impose different closure properties on the kernel.", "module lie", ["ring","nullspace","category"],visual="map",variants=["Module homomorphisms","Lie-algebra homomorphisms"])
E("operator","zero","Differential-operator kernel","Analysis · differential equations","Functions annihilated by an operator.",
  "The nullspace idea also applies to spaces of functions. The kernel of a differential operator consists of solutions of the corresponding homogeneous equation, in a specified function space and with any imposed boundary conditions.",
  "\\ker D=\\{f:Df=0\\}", "On an interval, the kernel of d/dx consists of constant functions. The kernel of the Laplacian consists of harmonic functions.",
  "A Green kernel represents a solution operator; it is not the nullspace of the differential operator. Domains and boundary conditions matter.", "operator", ["nullspace","green","integral"],visual="flat")
E("congruence","zero","Congruence / function kernel","Universal algebra · sets","Pairs of inputs that have the same output.",
  "Another convention calls the equivalence relation f(x)=f(y) the kernel of f. For a homomorphism of universal algebras, this relation is compatible with the algebra's operations: a congruence.",
  "\\ker f=\\{(x,y):f(x)=f(y)\\}", "For f(n)=n mod 3, the relation groups integers into three equivalence classes. It contains every pair differing by a multiple of 3.",
  "This kernel is a set of pairs, not just the zero equivalence class 3ℤ.", "congruence", ["group","kernel-pair"],visual="partition")
E("category","zero","Categorical kernel","Category theory","A universal arrow on which a morphism becomes zero.",
  "In a category with zero morphisms, a kernel of f:A→B is an arrow k:K→A that equalizes f and the zero arrow, with the corresponding universal property.",
  "\\ker f=\\operatorname{Eq}(f,0)", "For vector spaces, K is the usual nullspace and k includes it into A. Every map g with fg=0 factors uniquely through k.",
  "The categorical kernel includes a morphism and a universal property. Not every category has zero arrows or kernels.", "category", ["nullspace","module","kernel-pair"],visual="category")
E("kernel-pair","zero","Kernel pair","Category theory","The pullback that records inputs identified by a map.",
  "Where the relevant pullback exists, the kernel pair of f:A→B is A×ᵦA with its two projections to A. In sets it consists of pairs with equal f-images.",
  "A\\times_B A=\\{(x,y):f(x)=f(y)\\}", "The kernel pair of reduction modulo 3 records two integers whenever their residues agree.",
  "A kernel pair need not require a zero object. It generalizes the relation kernel, rather than the zero fiber alone.", "pair", ["congruence","category"],visual="partition")
E("isogeny","zero","Isogeny kernel","Elliptic curves · cryptography","Points mapped to the identity of another elliptic curve.",
  "An isogeny is a suitable group-preserving algebraic map between elliptic curves. Its point kernel over an algebraic closure is finite. For separable isogenies, the finite subgroup determines the quotient isogeny up to isomorphism.",
  "\\ker\\phi=\\{P:\\phi(P)=O\\}", "Over characteristic zero, the doubling map [2] has the identity and three nonzero 2-torsion points in its kernel.",
  "In positive characteristic, inseparability makes the distinction between geometric points and the kernel group scheme important.", "isogeny", ["group"],visual="partition",status="Specialization")
E("code","zero","Parity-check kernel","Coding theory","The nullspace describing all valid codewords.",
  "A linear code can be specified as the vectors annihilated by a parity-check matrix H over a finite field.",
  "C=\\ker H=\\{c:Hc^{\\mathsf T}=0\\}", "Over 𝔽₂, H=[1 1 1] defines {000, 011, 101, 110}: exactly the binary triples with even parity.",
  "Arithmetic is in the stated finite field, not ordinary real arithmetic. This is a use of the linear-algebra kernel.", "code", ["nullspace"],visual="bits",status="Specialization")

# Operator representations, local neighborhoods, and physical response functions.
E("integral","influence","Integral-operator kernel","Analysis","The two-variable function specifying an integral operator.",
  "A function K(x,y) describes how an input value at y contributes to an output at x. The operator integrates those contributions. More generally, a Schwartz kernel can be a distribution rather than an ordinary function.",
  "(Tf)(x)=\\int K(x,y)f(y)\\,dy", "For K(x,y)=xy on [0,1] and f(y)=y, the output is x∫₀¹y²dy=x/3.",
  "The function K and the nullspace ker(T) are both called kernels, even in the same discussion.", "schwartz", ["nullspace","convolution","green"],visual="matrix")
E("convolution","influence","Convolution kernel","Signals · analysis","A translated weighting function.",
  "Convolution is the translation-invariant case of an integral operator: K(x,y)=k(x−y). A single function k describes how the signal is mixed at every location.",
  "(f*k)(x)=\\int f(y)k(x-y)\\,dy", "A normalized box kernel averages nearby values. An impulse convolved with k reproduces k.",
  "Mathematical convolution reverses one operand relative to cross-correlation. Symmetric kernels hide this difference.", "convolve", ["filter","cnn","heat","reconstruction"],visual="wave")
E("filter","influence","Discrete image / signal kernel","Image processing · DSP","A small array of filter coefficients.",
  "A finite collection of weights samples the neighborhood around each output location. Blur, sharpening, derivatives and edge detection use different weight patterns.",
  "y[n]=\\sum_j k[j]x[n-j]", "The centered filter [¼, ½, ¼] changes a neighborhood [2, 8, 2] into the weighted value 5.",
  "Padding, origin, stride and whether the array is flipped affect the result. A filter need not be positive or normalized.", "convolve", ["convolution","cnn","morphology"],visual="filter",variants=["Box / Gaussian blur","Sobel and derivative filters","Laplacian / sharpening","Audio FIR filters"])
E("cnn","influence","CNN kernel / learned filter","Deep learning","A learned tensor of local filter weights.",
  "A convolution layer learns weights shared across spatial positions. With multiple channels, each output filter combines neighborhoods from the relevant input channels.",
  "Y_o[p,q]=b_o+\\sum_{c,i,j}W_{o,c,i,j}X_c[p+i,q+j]", "An ordinary Conv2d with 3 input channels, 8 output channels and 3×3 filters has weights shaped 8×3×3×3: 216 numbers, plus optional biases.",
  "PyTorch Conv2d implements cross-correlation. These weight tensors are distinct from the executable CPU or GPU kernels that apply them.", "cnn", ["filter","dispatch","cuda"],visual="filter")
E("morphology","influence","Morphological kernel","Image processing","A neighborhood shape, also called a structuring element.",
  "In morphology APIs, kernel often means a mask selecting the neighborhood for erosion, dilation, opening or closing. These operations need not be weighted sums.",
  "(f\\oplus B)(x)=\\max_{b\\in B}f(x-b)", "For binary dilation, a cross-shaped neighborhood expands a set in its four cardinal directions.",
  "A morphological kernel usually describes a shape or footprint. It is not generally a linear convolution filter.", "morph", ["filter","polygon"],visual="cross")
E("transform","influence","Transform kernel","Fourier · Laplace · integral transforms","The function against which a transform integrates.",
  "Integral transforms change a function's representation by integrating it against a prescribed function of the input and output coordinates.",
  "\\hat f(\\xi)=\\int f(x)e^{-2\\pi i x\\xi}\\,dx", "The Fourier kernel is e⁻²πⁱˣξ in this convention; the one-sided Laplace kernel is e⁻ˢᵗ on t≥0.",
  "A transform kernel may oscillate, be complex-valued, and have no probability or similarity interpretation. Fourier normalization conventions vary.", "transform", ["integral","cauchy","hilbert"],visual="oscillation",variants=["Fourier","Laplace","Hankel / Bessel transforms"])
E("green","influence","Green kernel / Green's function","PDE · mathematical physics","The response to a point source, with boundary conditions.",
  "A Green kernel represents an inverse or solution operator for a differential equation. Integrating the point-source responses builds the response to a distributed source.",
  "L_xG(x,y)=\\delta(x-y)", "For −u″=f on (0,1) with u(0)=u(1)=0, G(x,y)=min(x,y)−xy; then u(x)=∫₀¹G(x,y)f(y)dy.",
  "The operator, domain and boundary conditions are part of the definition. A Green kernel and an operator's nullspace are different.", "green", ["integral","operator","heat"],visual="green",variants=["Resolvent kernels","Fundamental solutions","Electrostatic / wave Green functions"])
E("heat","influence","Heat / diffusion kernel","PDE · probability","How a point concentration spreads over time.",
  "For heat diffusion in ℝᵈ, the fundamental solution is a normalized Gaussian whose width grows with time. Convolving it with initial data solves the homogeneous heat equation.",
  "H_t(z)=\\frac{e^{-\\|z\\|^2/(4Dt)}}{(4\\pi Dt)^{d/2}},\\quad t>0", "In one dimension, the distribution represented by Hₜ has variance 2Dt. More elapsed time produces a wider, lower peak.",
  "A heat kernel is a convolution kernel and, in suitable settings, a transition density. On a general manifold it is not a simple Gaussian of coordinate distance.", "heat", ["convolution","markov","gp"],visual="gaussian")
E("poisson","influence","Poisson kernel","Harmonic analysis · PDE","Weights that extend boundary values harmonically.",
  "A Poisson kernel solves a harmonic boundary-value problem by weighting boundary data. Its form depends on the domain.",
  "P_r(\\theta)=\\frac{1-r^2}{1-2r\\cos\\theta+r^2},\\quad 0\\le r<1", "In the unit disk, integrate Pᵣ against boundary values using dθ/(2π). At r=0, every boundary angle has equal weight.",
  "This Poisson kernel is unrelated to Poisson-distributed counts except through broader probabilistic connections.", "poissondisk", ["green","cauchy"],visual="circle")
E("dirichlet","influence","Dirichlet kernel","Fourier analysis","The convolution kernel for a Fourier partial sum.",
  "Adding the frequency modes from −N through N produces a kernel that reconstructs the Nth Fourier partial sum.",
  "D_N(\\theta)=\\sum_{n=-N}^{N}e^{in\\theta}=\\frac{\\sin((N+1/2)\\theta)}{\\sin(\\theta/2)}", "D₁(θ)=1+2cosθ. Its oscillating lobes help explain why partial sums can overshoot near jumps.",
  "It is not everywhere positive and is not a probability density. Its name does not make it the general kernel for a Dirichlet boundary problem.", "fourier", ["fejer","transform"],visual="sinc")
E("fejer","influence","Fejér kernel","Fourier analysis","The nonnegative kernel for averaged Fourier sums.",
  "Averaging the first N+1 Dirichlet kernels gives a nonnegative approximation kernel with good convergence properties for continuous periodic functions.",
  "F_N(\\theta)=\\frac1{N+1}\\left(\\frac{\\sin((N+1)\\theta/2)}{\\sin(\\theta/2)}\\right)^2", "For N=1, F₁(θ)=1+cosθ. Its integral with normalized circle measure is 1.",
  "Cesàro averaging changes the kernel, rather than simply adding more Fourier modes.", "fourier", ["dirichlet","mollifier"],visual="positive")
E("mollifier","influence","Mollifier / approximate-identity kernel","Analysis · numerical smoothing","A scaled kernel that smooths while approaching the identity.",
  "A standard mollifier is a smooth, nonnegative, unit-integral bump. Shrinking its scale gives a family whose convolution approximates the original function. Approximate identities form a broader class.",
  "\\rho_\\varepsilon(x)=\\varepsilon^{-d}\\rho(x/\\varepsilon)", "Convolving a step with a small smooth bump replaces the jump with a narrow smooth transition.",
  "Not every smoothing filter is an approximate identity, and not every approximate identity is a compactly supported smooth mollifier.", "mollify", ["convolution","heat"],visual="gaussian")
E("singular","influence","Singular / Calderón–Zygmund kernel","Harmonic analysis","An operator kernel singular along the diagonal.",
  "Singular integral kernels can blow up as x approaches y. Cancellation, principal values and suitable boundedness and regularity conditions make the corresponding operators meaningful.",
  "|K(x,y)|\\lesssim |x-y|^{-d}", "The Hilbert-transform kernel is the one-dimensional prototype. Riesz transforms provide higher-dimensional examples.",
  "An arbitrary divergent integral is not automatically a valid singular integral operator.", "singular", ["hilbert","cauchy","integral"],visual="singular")
E("hilbert","influence","Hilbert-transform kernel","Signals · harmonic analysis","A principal-value 1/x kernel.",
  "The Hilbert transform uses an odd singular kernel to construct a quadrature counterpart of a real signal. Its convolution is interpreted in the principal-value sense.",
  "Hf(x)=\\frac1\\pi\\operatorname{p.v.}\\int\\frac{f(y)}{x-y}\\,dy", "In a standard convention, H(cosωx)=sinωx for ω>0. This is useful in analytic-signal representations.",
  "Normalization and sign conventions vary. This is not the reproducing kernel of an arbitrary Hilbert space.", "hilbert", ["singular","transform","rkhs"],visual="singular")
E("cauchy","influence","Cauchy kernel","Complex analysis","The reciprocal kernel in Cauchy's integral formula.",
  "Cauchy's formula recovers a holomorphic function from its values on a surrounding contour by integrating against a reciprocal factor.",
  "f(z)=\\frac1{2\\pi i}\\oint\\frac{f(\\zeta)}{\\zeta-z}\\,d\\zeta", "For f(ζ)=ζ² on a contour surrounding z, the integral returns z².",
  "The contour orientation and the location of z matter. A Cauchy kernel is not the same object as a Cauchy probability density.", "cauchy", ["transform","szego","poisson"],visual="circle")
E("kde","influence","Density-estimation kernel","Statistics","A normalized bump placed at each observation.",
  "Kernel density estimation adds rescaled copies of a kernel around observed samples to estimate a density. Bandwidth sets the smoothing scale.",
  "\\hat p_h(x)=\\frac1{nh}\\sum_{i=1}^n K\\left(\\frac{x-x_i}{h}\\right)", "Place one Gaussian bump at each sample, then average the bumps. Smaller h reveals more detail and more sample noise.",
  "A classical density kernel integrates to 1. It need not be a positive-semidefinite similarity kernel; higher-order estimation kernels can even have negative parts.", "kde", ["regression","rbf","likelihood"],visual="density",variants=["Gaussian","Epanechnikov","Uniform / box","Triangular"])
E("regression","influence","Kernel-regression weights","Statistics","Weights for fitting or averaging nearby observations.",
  "In Nadaraya–Watson regression, a kernel assigns locality weights and their normalized sum gives a predicted mean. Local polynomial regression uses related weights in a local fit.",
  "\\hat m(x)=\\frac{\\sum_i K_h(x-x_i)y_i}{\\sum_i K_h(x-x_i)}", "If two response values 10 and 20 receive weights 3 and 1, the local constant prediction is 12.5.",
  "This local smoother differs from kernel ridge regression in an RKHS, although both may use Gaussian functions.", "regression", ["kde","rkhs"],visual="density")
E("reconstruction","influence","Interpolation / reconstruction kernel","Graphics · DSP","A function used to reconstruct values between samples.",
  "A reconstruction kernel builds a continuous approximation from discrete samples. The kernel shape controls sharpness, smoothness and ringing.",
  "\\tilde f(x)=\\sum_n f[n]h(x-n)", "A triangular kernel gives linear interpolation in one dimension. Ideal bandlimited reconstruction uses sinc(x)=sin(πx)/(πx).",
  "Exact sinc reconstruction requires the sampling theorem's assumptions. Bicubic and Lanczos filters are practical alternatives with different tradeoffs.", "reconstruct", ["convolution","filter"],visual="sinc",variants=["Nearest neighbor / box","Tent / bilinear","Bicubic","Sinc / Lanczos"])
E("probability","influence","Measure / probability kernel","Measure theory · probability","A measurable assignment of a measure to each input.",
  "A measure kernel assigns a measure K(x,·) to every x, measurably in x. A probability kernel assigns probability measures. Densities are optional, not part of the general definition.",
  "K:X\\times\\mathcal B(Y)\\to[0,\\infty]", "K(x,B)=δₓ(B) describes deterministic copying of x: all probability is concentrated at x.",
  "K(x,B) takes a measurable set as its second argument. A density k(x,y), when one exists, is a representation of this kernel.", "probability", ["markov","heat"],visual="probability",variants=["Stochastic kernels","Conditional-distribution kernels","Randomization kernels","Communication-channel kernels"])
E("markov","influence","Markov transition kernel","Stochastic processes · MCMC","The distribution of the next state, given the current state.",
  "A transition kernel specifies a Markov step. On a finite state space, it is a nonnegative row-stochastic matrix; on general spaces it is a probability kernel.",
  "P(x,B)=\\Pr(X_{t+1}\\in B\\mid X_t=x)", "For P=[[0.8,0.2],[0.3,0.7]], state 0 transitions to state 1 with probability 0.2. Every row sums to 1.",
  "A Markov kernel need not be symmetric or positive semidefinite. An SVM kernel has different requirements.", "markov", ["probability","psd","dispersal"],visual="probability",variants=["MCMC proposal / transition kernels","Feller kernels","Diffusion transition densities"])
E("likelihood","influence","Density / likelihood kernel","Bayesian statistics","A density or likelihood with irrelevant constants removed.",
  "In statistical calculations, kernel can mean the part of a density or likelihood left after factors constant in the variable of interest are dropped.",
  "p(\\theta)\\propto g(\\theta)", "For a normal density with fixed variance, viewed as a function of μ, exp(−(x−μ)²/(2σ²)) is its likelihood kernel.",
  "Constant means constant in the variable being studied. If σ is unknown, the 1/σ factor cannot be discarded.", "likelihood", ["kde","probability"],visual="gaussian")
E("stein-prob","influence","Stein kernel: integration by parts","Probability · normal approximation","A function or matrix realizing a Stein identity.",
  "For a one-dimensional variable X with mean μ, a Stein kernel τ satisfies an integration-by-parts identity for suitable test functions.",
  "\\mathbb E[(X-\\mu)f(X)]=\\mathbb E[\\tau(X)f'(X)]", "For X∼N(μ,σ²), the constant τ(x)=σ² is a Stein kernel. For a uniform variable on [−1,1], τ(x)=(1−x²)/2.",
  "This τ is a function of one input. The pairwise Stein kernel used in a kernel Stein discrepancy is another construction.", "steinprob", ["stein-ml","likelihood"],visual="flat")
E("volterra","influence","Volterra-series kernel","Nonlinear systems · control","A higher-order impulse-response function.",
  "A Volterra expansion expresses a nonlinear system through kernels of one, two or more time lags, multiplying corresponding input values before integration.",
  "y_2(t)=\\iint h_2(\\tau_1,\\tau_2)x(t-\\tau_1)x(t-\\tau_2)\\,d\\tau_1d\\tau_2", "A quadratic response requires a two-lag kernel h₂, whereas an LTI system uses a one-lag impulse response h₁.",
  "Volterra can also describe a linear integral operator with a variable integration limit. That usage is an integral-kernel subtype.", "volterra", ["convolution","memory"],visual="matrix")
E("memory","influence","Memory / friction kernel","Statistical mechanics · systems","Weights on the system's past behavior.",
  "A memory kernel specifies how past states or velocities influence present evolution. Generalized Langevin equations use such kernels to describe non-instantaneous friction.",
  "F_{\\rm mem}(t)=-\\int_0^t\\Gamma(t-s)v(s)\\,ds", "With Γ(t)=γe⁻ᵗ/τ, recent velocities receive greater weight than distant ones.",
  "This is a temporal response function, not a block of computer memory or a GPU routine.", "memory", ["volterra","convolution"],visual="decay")
E("dispersal","influence","Dispersal kernel","Ecology · population dynamics","A distribution of dispersal displacement or distance.",
  "A dispersal kernel describes where seeds, spores or organisms arrive relative to their source. Its tails strongly affect long-range spread.",
  "n_{t+1}(x)=\\int k(x-y)g(n_t(y))\\,dy", "A narrow Gaussian models mostly local movement; a heavy-tailed distribution allows more rare long-distance arrivals.",
  "A distance density and a density per unit area differ by a radial Jacobian. Always check the units and normalization.", "dispersal", ["markov","convolution","grain"],visual="gaussian")
E("collision","influence","Collision / coagulation kernel","Aerosols · kinetic theory · materials","A rate describing pair interactions.",
  "A coagulation kernel K(a,b) gives the rate at which particles of sizes a and b merge in a population-balance model. Collision kernels in kinetic equations likewise encode interaction rates.",
  "\\text{pair-event rate}\\ \\propto\\ K(a,b)n(a)n(b)", "The constant coagulation kernel assigns the same size-independent rate to every pair; additive and multiplicative kernels weight sizes differently.",
  "Nonnegative interaction rates do not imply a positive-semidefinite ML kernel. Physical units are rate units, not similarity units.", "collision", ["integral","psd","flame"],visual="matrix",variants=["Smoluchowski coagulation","Boltzmann collision kernels","Fragmentation kernels"])
E("sensitivity","influence","Sensitivity / Fréchet kernel","Geophysics · inverse problems","How a model perturbation changes an observation.",
  "Linearizing a forward model produces a sensitivity kernel: a spatial weighting of parameter perturbations that predicts a small data change.",
  "\\delta d\\approx\\int K_d(r)\\,\\delta m(r)\\,dr", "A seismic travel-time kernel indicates which regions of Earth's structure influence a measurement. Finite-frequency sensitivity can occupy a volume rather than a single ray.",
  "It represents a derivative of the forward model, not necessarily the resolution of a retrieved model.", "sensitivity", ["averaging","integral"],visual="sensitivity")
E("averaging","influence","Averaging / resolution kernel","Remote sensing · inverse problems","How the true state appears in a retrieved state.",
  "An averaging kernel differentiates the retrieval with respect to the true state. It describes sensitivity and smoothing in a recovered atmospheric profile or other inverse solution.",
  "A=\\frac{\\partial\\hat x}{\\partial x}", "A retrieved value at one altitude may average the true state over nearby altitudes. An ideal noiseless, fully resolved retrieval has A=I.",
  "Averaging kernels need not be simple positive averages. They differ from the forward measurement's sensitivity kernel.", "averaging", ["sensitivity","integral"],visual="matrix")
E("shield","influence","Radiation point kernel","Radiation transport · shielding","The detector response to a point radiation source.",
  "Point-kernel methods integrate point-source responses over a distributed radiation source. A basic uncollided photon-flux term combines geometric spreading and attenuation; buildup models can approximate scattered contributions.",
  "K(r)=\\frac{e^{-\\mu r}}{4\\pi r^2}", "In a homogeneous absorber, the uncollided response falls with inverse-square distance and exponential attenuation.",
  "Real shielding calculations require energy, material, geometry and scattering considerations. This formula is an illustrative idealization, not a shield-design prescription.", "shield", ["green","fuel"],visual="decay")
E("xc","influence","Exchange–correlation kernel","Quantum chemistry · TDDFT","A functional derivative of a potential with respect to density.",
  "The exchange–correlation response kernel relates a small electron-density change to a change in the exchange–correlation potential.",
  "f_{xc}(r,t;r',t')=\\frac{\\delta v_{xc}(r,t)}{\\delta n(r',t')}", "An adiabatic local approximation yields a response local in time and space, represented using delta factors and a density-dependent derivative.",
  "This is a response function in density-functional theory, not the core electrons of the historical atomic kernel.", "xc", ["sensitivity","atomic"],visual="matrix")
E("bethe","influence","Bethe–Salpeter interaction kernel","Particle physics · many-body theory","The interaction part of a two-particle integral equation.",
  "The Bethe–Salpeter framework uses an interaction kernel to couple two-particle amplitudes. Approximations to it determine which interaction contributions the model includes.",
  "\\Gamma=K\\,G_0\\,\\Gamma\\quad\\text{(schematic bound-state equation)}", "A ladder approximation retains repeated exchanges built from an elementary exchange kernel.",
  "This is a schematic operator equation; propagator factors, indices and integration conventions vary by formulation.", "bethe", ["integral","green"],visual="matrix")
E("kpm","influence","Kernel polynomial method","Computational condensed matter","A damping kernel for truncated polynomial expansions.",
  "Kernel polynomial methods damp coefficients of truncated Chebyshev expansions to reduce oscillations and obtain useful spectral approximations.",
  "f_N(x)=\\sum_{n=0}^N g_n\\mu_nT_n(x)\\quad\\text{(schematic)}", "Jackson damping suppresses ringing in approximate densities of states. Dirichlet and Lorentz kernels give other damping choices.",
  "The displayed series omits application-specific prefactors and normalization. The kernel concerns the expansion, not GPU execution.", "kpm", ["dirichlet","fejer","compute-cpu"],visual="sinc",variants=["Jackson","Lorentz","Dirichlet"])

# Positive-semidefinite pairwise functions and their important specializations.
E("psd","similarity","Positive-semidefinite kernel","ML · analysis","A pairwise function whose Gram matrices are PSD.",
  "For a real symmetric kernel k, every finite Gram matrix must be positive semidefinite. This makes k representable as an inner product in a feature space.",
  "\\sum_{i,j}a_ia_jk(x_i,x_j)\\ge0", "The ordinary dot product is a kernel: k(x,y)=xᵀy. More elaborate kernels let algorithms use implicit feature spaces.",
  "A plausible similarity score is not automatically a valid PSD kernel. Literature often says positive definite while allowing semidefinite Gram matrices.", "svm", ["rkhs","markov","rbf"],visual="gram",variants=["Mercer kernels (under appropriate hypotheses)","SVM and kernel ridge regression","Kernel PCA"])
E("rkhs","similarity","Reproducing kernel","Functional analysis","A pairwise function that reproduces evaluation.",
  "In a reproducing kernel Hilbert space, evaluation is an inner product with a distinguished kernel section. Every positive-semidefinite kernel determines an associated RKHS.",
  "f(x)=\\langle f,k(x,\\cdot)\\rangle_{\\mathcal H}", "If k(x,y)=xy on ℝ, the associated functions have the form f(x)=ax; pairing with k(x,·) recovers ax.",
  "Not every Hilbert space of functions is an RKHS: point evaluation must be a bounded functional.", "rkhs", ["psd","bergman","szego","mmd"],visual="gram")
E("gp","similarity","Covariance kernel","Gaussian processes · random fields","The covariance between indexed random variables.",
  "A covariance kernel expresses how fluctuations at two inputs co-vary. For a Gaussian process, a mean function and a valid covariance kernel specify all finite-dimensional distributions.",
  "k(x,y)=\\operatorname{Cov}(f(x),f(y))", "A long length scale in an RBF covariance makes nearby observations strongly correlated; a shorter scale allows faster variation.",
  "A covariance may be negative at some pairs while its Gram matrices remain PSD. Positive entrywise values and positive semidefiniteness are different properties.", "gp", ["psd","rbf","nngp"],visual="gram")
E("rbf","similarity","Gaussian / RBF similarity kernel","Machine learning","Exponentially decreasing similarity in squared distance.",
  "The Gaussian radial-basis-function kernel compares points using their squared Euclidean distance and a scale parameter. It is a standard PSD kernel.",
  "k(x,y)=\\exp\\left(-\\frac{\\|x-y\\|^2}{2\\ell^2}\\right)", "At distance ℓ, similarity is e⁻¹/²≈0.607. At zero distance it is 1.",
  "The same Gaussian shape appears in heat flow, KDE and image blur. Their arguments, units and normalization differ.", "pairwise", ["kde","heat","filter","gp"],visual="gaussian",status="Named kernel")
E("kernel-families","similarity","Named similarity-kernel families","Machine learning · Gaussian processes","Different constructions inside the PSD family.",
  "Linear, polynomial, Laplacian, Matérn, rational-quadratic and periodic kernels encode different notions of features, smoothness or repetition.",
  "k_{\\rm poly}(x,y)=(\\gamma x^{\\mathsf T}y+c)^d", "For γ=1, c=0 and d=2, the polynomial kernel equals the dot product of quadratic feature vectors.",
  "Parameters and domains matter. The sigmoid formula tanh(γxᵀy+c), although offered by software APIs, is not PSD for arbitrary parameters.", "gp pairwise", ["psd","rbf","graph-ml"],visual="features",variants=["Linear","Polynomial","Laplacian","Matérn","Rational quadratic","Periodic","Histogram / χ² kernels"])
E("graph-ml","similarity","Graph kernel: machine learning","Graph ML","A similarity kernel between whole graphs.",
  "Graph kernels use features such as walks, subgraphs or neighborhood patterns to compare graph-structured inputs within kernel methods.",
  "k(G,H)=\\langle\\phi(G),\\phi(H)\\rangle", "A simple kernel compares vectors counting vertex labels. Richer kernels compare shared walks or Weisfeiler–Lehman patterns.",
  "A graph-theory kernel is a selected vertex set in a single digraph; a graph ML kernel compares two graph objects.", "graphml", ["digraph","psd","string"],visual="graph")
E("string","similarity","String / sequence kernel","Bioinformatics · NLP","An inner-product comparison of sequence features.",
  "String kernels compare sequences through features such as counts of substrings or subsequences, often without explicitly constructing the full feature vectors.",
  "k(s,t)=\\sum_u\\operatorname{count}_s(u)\\operatorname{count}_t(u)", "For length-2 substring counts, AABA has AA, AB and BA once each. Comparing these counts gives a simple spectrum kernel.",
  "This is a similarity function for sequences, not a text-processing routine or language runtime.", "string", ["psd","fisher","graph-ml"],visual="bits")
E("fisher","similarity","Fisher kernel","Statistical machine learning","Similarity between model-score vectors.",
  "A generative model provides score features: gradients of log likelihood with respect to its parameters. The Fisher kernel compares those features using an information-based metric.",
  "k(x,y)=U_x^{\\mathsf T}I^{-1}U_y,\\quad U_x=\\nabla_\\theta\\log p_\\theta(x)", "Two observations are similar when they suggest similar parameter changes in the chosen generative model.",
  "The model and parameterization are part of the construction; an inverse or suitable generalized inverse requires care.", "fisher", ["psd","likelihood","ntk"],visual="features")
E("ntk","similarity","Neural tangent kernel","Deep-learning theory","Inner products of parameter gradients.",
  "For a scalar network output, the NTK compares gradients of the output with respect to model parameters. It describes local function changes during training.",
  "\\Theta_\\theta(x,y)=\\langle\\nabla_\\theta f_\\theta(x),\\nabla_\\theta f_\\theta(y)\\rangle", "For fθ(x)=θx, the NTK is xy. For a finite nonlinear network, it generally changes as θ changes.",
  "The limiting constant-kernel training description requires specific infinite-width assumptions. An arbitrary finite network is not automatically in that regime.", "ntk", ["nngp","fisher","psd"],visual="gram")
E("nngp","similarity","Neural-network GP kernel","Deep-learning theory","Output covariance from a random network.",
  "Randomly initialized networks can induce covariance kernels. Under suitable infinite-width conditions, their outputs converge to a Gaussian process with a network-dependent kernel.",
  "k(x,y)=\\mathbb E[f_\\theta(x)f_\\theta(y)]\\quad\\text{(zero mean)}", "For fθ(x)=θx with θ∼N(0,1), the induced covariance is xy.",
  "The NNGP kernel uses random outputs; the NTK uses parameter gradients. Their roles and formulas differ.", "ntk", ["ntk","gp"],visual="gram")
E("mmd","similarity","Kernel mean / distribution embedding","Statistics · machine learning","Represent a distribution by an average kernel section.",
  "A kernel mean embedding averages feature representations under a distribution. Distances between such embeddings produce the maximum mean discrepancy (MMD).",
  "\\mu_P=\\mathbb E_{X\\sim P}[k(X,\\cdot)]", "With a linear kernel, the embedding captures the ordinary mean. A characteristic kernel can distinguish all probability distributions in an appropriate class.",
  "Kernel here is still the underlying pairwise PSD function; the mean embedding is a derived object. Moment and measurability assumptions apply.", "mmd", ["rkhs","probability"],visual="density",status="Derived construction")
E("stein-ml","similarity","Stein kernel: pairwise discrepancy","Statistical ML","An RKHS kernel transformed by Stein operators.",
  "Applying a distribution's Stein operator to both arguments of a base kernel produces a pairwise kernel used to assess sample fit, often without a density's normalizing constant.",
  "k_p(x,y)=\\mathcal T_p^x\\mathcal T_p^y k(x,y)\\quad\\text{(schematic)}", "A kernel Stein discrepancy combines density scores and derivatives of an RBF kernel to compare a sample with a model.",
  "This pairwise function is distinct from the one-input integration-by-parts Stein kernel τ(x). Boundary and regularity conditions matter.", "steinml", ["stein-prob","rkhs","likelihood"],visual="gram")
E("quantum","similarity","Quantum feature kernel","Quantum machine learning","Similarity defined by encoded quantum states.",
  "A quantum feature map encodes an input into a state. A common kernel is the squared overlap of two encoded states, also interpretable as an inner product of density operators.",
  "k(x,y)=|\\langle\\psi(x)|\\psi(y)\\rangle|^2", "Identical pure states give similarity 1; orthogonal states give 0.",
  "This is a kernel method implemented or estimated with quantum circuits. A useful quantum advantage does not follow merely from the definition.", "quantum", ["psd"],visual="gram")
E("bergman","similarity","Bergman kernel","Complex analysis","The reproducing kernel for square-integrable holomorphic functions.",
  "The Bergman kernel reproduces holomorphic functions in an L² space on a complex domain and represents the Bergman projection.",
  "B_{\\mathbb D}(z,w)=\\frac1{\\pi(1-z\\bar w)^2}", "On the unit disk with ordinary area measure, integrating B(z,w)f(w) over the disk recovers f(z) for suitable holomorphic f.",
  "The domain and measure normalization determine the formula. It is both an integral kernel and a reproducing kernel.", "bergman", ["rkhs","szego","integral"],visual="circle")
E("szego","similarity","Szegő kernel","Complex analysis","A reproducing kernel for a Hardy-space setting.",
  "The Szegő kernel reproduces functions in a Hardy space, using boundary rather than area-based data in the standard disk setting.",
  "S_{\\mathbb D}(z,w)=\\frac1{1-z\\bar w}", "With normalized boundary measure dθ/(2π), the disk Hardy-space kernel is 1/(1−z w̄).",
  "Normalization varies. The Szegő and Bergman kernels reproduce different function spaces; they are not interchangeable.", "szego", ["bergman","cauchy","rkhs"],visual="circle")
E("determinantal","similarity","Determinantal / correlation kernel","Random matrices · probability","A kernel whose determinants encode joint point correlations.",
  "Determinantal point processes express their correlation functions as determinants of matrices built from a kernel. Famous scaling limits include the sine, Airy and Bessel kernels.",
  "\\rho_n(x_1,\\ldots,x_n)=\\det[K(x_i,x_j)]_{i,j=1}^n", "The sine kernel is sin(π(x−y))/(π(x−y)), with diagonal value 1, in a common bulk-scaling convention.",
  "Not every PSD kernel defines a valid determinantal process. Operator constraints and the reference measure also matter.", "dpp", ["rkhs","probability","reconstruction"],visual="sinc",variants=["Sine","Airy","Bessel"])

# Structurally distinguished regions and sets.
E("digraph","subset","Digraph kernel","Graph theory · combinatorial games","An independent, absorbing set of vertices.",
  "A digraph kernel is a vertex set with no arcs between its members, such that every vertex outside it has an outgoing arc to a member.",
  "\\forall v\\notin K\\;\\exists k\\in K:\\ v\\to k", "For the chain a→b→c, {a,c} is a kernel: it is independent, and b points to c. A directed 3-cycle has no kernel.",
  "Absorption uses outgoing arcs in this convention. A maximal independent set alone is insufficient in a directed graph.", "digraph", ["graph-ml","kernelization"],visual="digraph",variants=["Quasi-kernels (distance ≤2)","k-kernels","Kernels by paths / colored kernels"])
E("polygon","subset","Visibility kernel","Computational geometry","All points that can see the entire shape.",
  "The kernel of a polygon or suitable polyhedron consists of points from which every point of the shape is visible along a segment staying inside it.",
  "\\ker P=\\{p\\in P:[p,q]\\subseteq P\\ \\forall q\\in P\\}", "A convex polygon's kernel is the whole polygon. For a simple star-shaped polygon, intersect the interior half-planes of its edges.",
  "The kernel can be empty. A CGAL geometry kernel is software machinery, not this visible region.", "polygon", ["cgal","viability","kern"],visual="region")
E("viability","subset","Viability kernel","Control · dynamical systems","Initial states from which some safe evolution exists.",
  "Within a constraint set, the viability kernel contains states for which at least one admissible evolution stays in the set for the specified horizon, often forever.",
  "\\operatorname{Viab}(C)=\\{x_0:\\exists\\text{ admissible safe evolution}\\}", "For a vehicle near a wall, safety depends on position and velocity: some positions are already unrecoverable if the vehicle is moving too quickly.",
  "This is an existence guarantee under a model and control constraints. It does not mean every possible control is safe.", "viability", ["discriminating","polygon"],visual="region")
E("discriminating","subset","Discriminating / robust safety kernel","Control · differential games","States from which safety can be maintained against disturbances.",
  "A discriminating kernel strengthens viability by introducing a disturbance or opponent. Safety must be preserved using an appropriate control strategy under the stated information pattern.",
  "\\exists\\text{ control strategy}\\ \\forall\\text{ admissible disturbances}", "A robot's safe region shrinks when the model must tolerate an adversarial wind rather than one favorable wind trajectory.",
  "Quantifier order, when disturbances are observed, and strategy definitions are essential. Robust-control terminology varies across formulations.", "discriminate", ["viability"],visual="region")
E("perfect","subset","Perfect kernel","Topology · descriptive set theory","The perfect part left after removing isolated points.",
  "Cantor–Bendixson analysis repeatedly removes isolated points, possibly through transfinite stages. In a Polish-space setting, the remaining perfect part is called the perfect kernel.",
  "X=P\\sqcup C,\\quad P\\text{ perfect},\\ C\\text{ countable}", "For the Cantor set together with one isolated point outside it, the perfect kernel is the Cantor set.",
  "Perfect means closed with no isolated points. Removing isolated points only once need not reach the perfect kernel.", "perfect", ["saturation","semigroup"],visual="cantor")
E("saturation","subset","Topological set kernel","General topology","The intersection of all open supersets of a set.",
  "Some topology literature calls the saturation of A its kernel: the points that cannot be excluded by any open set containing A.",
  "\\ker A=\\bigcap\\{U:A\\subseteq U,\\ U\\text{ open}\\}", "In the Sierpiński space with open sets ∅, {1}, {0,1}, the kernel of {0} is {0,1}.",
  "This construction can enlarge A. In a T₁ space it equals A, and it differs from the perfect kernel.", "saturation", ["perfect"],visual="region",status="Less-common usage")
E("semigroup","subset","Semigroup kernel","Semigroup theory","The intersection of nonempty two-sided ideals.",
  "The kernel of a semigroup is its least nonempty ideal when such an ideal exists; one can define it as the intersection of all nonempty ideals. A nonempty finite semigroup has such an ideal.",
  "K(S)=\\bigcap_{I\\ne\\varnothing\\,\\text{ideal}}I", "If a semigroup has an absorbing zero element, {0} is an ideal contained in every nonempty ideal, so it is the kernel.",
  "This kernel belongs to the semigroup itself. A semigroup homomorphism's congruence kernel belongs to a map.", "semigroup", ["congruence","perfect"],visual="core")
E("radical","subset","Squarefree kernel / integer radical","Number theory","The product of distinct prime divisors.",
  "A common convention defines the squarefree kernel of n as its radical: the largest squarefree divisor of a positive integer n.",
  "\\operatorname{rad}(n)=\\prod_{p\\mid n}p", "72=2³·3², so rad(72)=2·3=6. By contrast, the squarefree part in 72=m²s is s=2.",
  "Terminology varies: some sources use squarefree kernel for the squarefree part instead. Check the explicit formula.", "radical", ["ring"],visual="factors",status="Terminology varies")
E("belief","subset","Belief-revision kernel","Logic · knowledge representation","A minimal set of beliefs that entails a target.",
  "An α-kernel of a belief base is an inclusion-minimal subset that implies α. Kernel contraction removes at least one belief from each such subset to stop deriving α.",
  "B\\perp\\!\\perp\\alpha=\\{X\\subseteq B:X\\models\\alpha,\\ X\\text{ minimal}\\}", "For B={p, p→q, q}, the q-kernels are {q} and {p,p→q}. Removing only the explicit q leaves the second proof intact.",
  "A kernel is inclusion-minimal, not necessarily smallest by cardinality. This has no connection to Lean's trusted checker beyond both occurring in logic.", "belief", ["lean"],visual="reduce")
E("game","subset","Cooperative-game kernel / prekernel","Game theory","Payoff allocations balanced by pairwise bargaining power.",
  "Davis and Maschler's kernel is a solution concept for transferable-utility games. It uses each player's maximum surplus against another, with qualifications for individual-rationality boundaries.",
  "s_{ij}(x)=\\max_{S\\ni i,\\ S\\not\\ni j}\\left(v(S)-\\sum_{k\\in S}x_k\\right)", "In a symmetric three-player game where only the grand coalition has value 1, the equal split (⅓,⅓,⅓) balances every pair's maximum surplus.",
  "The prekernel enforces equality of pairwise maximum surpluses. The kernel's boundary conditions differ. Neither is the game's core or a digraph vertex kernel.", "games", ["digraph"],visual="graph")
E("kernel-search","subset","Kernel Search","Operations research · MILP","A selected variable subset used by an optimization heuristic.",
  "Kernel Search builds and expands a promising subset of decision variables, solving restricted mixed-integer problems while examining additional variable groups.",
  "\\text{restricted MILP on selected variables }K", "In portfolio optimization, begin with a small set of promising assets and test further asset groups to improve the feasible portfolio.",
  "This is a heuristic. It does not imply an equivalent instance of parameter-bounded size, as formal kernelization does.", "ks", ["kernelization"],visual="reduce",status="Named method")
E("kern","subset","Section kern / core","Structural mechanics","The load region that keeps a section in compression.",
  "The kern of a cross-section is the region in which an eccentric compressive force can act without creating tensile stress, within the assumed linear stress model.",
  "|e|\\le b/6\\quad\\text{(one-axis rectangular-section condition)}", "For eccentricity along one axis of a rectangle, the familiar middle-third condition avoids tension.",
  "The standard English term is usually kern, not kernel. It is included as a closely related STEM term; a rectangular section's full two-axis kern is a diamond.", "kern", ["polygon"],visual="kern",status="Related term: kern")

# Executable numerical routines.
E("cuda","compute","CUDA kernel","GPU programming","A device function launched over a grid of threads.",
  "A CUDA kernel is a GPU entry-point function. A launch specifies a grid of thread blocks; thread indices let each invocation work on a different portion of the input.",
  "i=\\text{blockIdx.x}\\cdot\\text{blockDim.x}+\\text{threadIdx.x}", "For vector addition, each in-range thread computes c[i]=a[i]+b[i]. A bounds check handles a final partially used block.",
  "The routine can compute any supported operation. It need not be a convolution or an ML similarity kernel.", "cuda", ["cnn","hip","triton","fusion"],visual="grid",code="__global__ void add(const float* a, const float* b,\n                    float* c, int n) {\n  int i = blockIdx.x * blockDim.x + threadIdx.x;\n  if (i < n) c[i] = a[i] + b[i];\n}\n// Device pointers assumed; n > 0.\nadd<<<(n + 255) / 256, 256>>>(a, b, c, n);")
E("opencl","compute","OpenCL kernel","Heterogeneous computing","An entry point executed by OpenCL work-items.",
  "OpenCL C marks kernel entry points with __kernel or kernel. Work-items are organized into work-groups over an index space, called an NDRange.",
  "i=\\operatorname{get\\_global\\_id}(0)", "A vector-add work-item reads a[i] and b[i] and writes c[i], with i obtained from its global ID.",
  "OpenCL kernels can target supported device types beyond GPUs. A work-group is analogous to, but not identical in all details to, a CUDA block.", "opencl", ["cuda","shader"],visual="grid")
E("metal","compute","Metal compute kernel","Apple GPU programming","A Metal function with the kernel entry-point attribute.",
  "Metal distinguishes vertex, fragment and kernel entry points. A compute kernel runs threads arranged into threadgroups and a grid.",
  "i=\\text{thread\\_position\\_in\\_grid}", "A Metal compute function can add vectors or apply an image operation on an Apple GPU.",
  "The word kernel selects a compute entry point in the language. Vertex and fragment entry points have different roles.", "metal", ["cuda","shader","filter"],visual="grid")
E("hip","compute","HIP kernel","AMD · portable GPU programming","A GPU entry point in the HIP programming model.",
  "HIP uses CUDA-like C++ syntax and a thread/block model. A __global__ function denotes a device kernel entry point.",
  "i=\\text{blockIdx.x}\\cdot\\text{blockDim.x}+\\text{threadIdx.x}", "A vector-add kernel uses the same familiar global-index pattern, while HIP supplies the relevant compilation and runtime layer.",
  "This is the executable-computation meaning of kernel; portability does not make hardware performance or every implementation detail identical.", "hip", ["cuda","opencl"],visual="grid")
E("shader","compute","Compute shader / compute kernel","Graphics · GPGPU","A parallel compute entry point dispatched by a graphics API.",
  "Compute shaders run invocations in workgroups, without requiring the vertex-to-fragment graphics pipeline. Some tools and discussions call these compute kernels.",
  "i=\\text{global invocation ID}", "A Vulkan compute dispatch can update particles or multiply arrays; each invocation uses its ID to find its work.",
  "A shader is not always a compute kernel: vertex and fragment shaders serve different pipeline stages.", "shader", ["metal","opencl","cuda"],visual="grid",status="API-dependent terminology")
E("triton","compute","Triton kernel","Deep-learning infrastructure","A program written for tiled GPU computation.",
  "Triton kernels express operations on blocks of elements. Program IDs divide work into tiles, while the compiler maps those block operations to device execution.",
  "\\text{offsets}=\\text{program ID}\\cdot B+[0,\\ldots,B-1]", "A block-vector-add program loads B positions, masks out-of-range offsets, adds the values and stores a tile.",
  "A Triton program is not one scalar CUDA thread. The programming abstraction exposes blocks of data.", "triton", ["cuda","pallas","fusion"],visual="tiles")
E("pallas","compute","Pallas kernel","JAX · GPU / TPU programming","A custom accelerator routine expressed through JAX APIs.",
  "Pallas provides lower-level kernel programming with explicit memory access and division of work across accelerator compute units. It supports GPU and TPU programming through backend-dependent paths.",
  "\\text{input refs}\\longmapsto\\text{output refs}", "A vector-add kernel loads tiles from references, adds them with JAX array operations, and writes an output tile.",
  "An ordinary JAX function is not itself necessarily a single Pallas or hardware kernel. Backends and experimental APIs evolve.", "pallas", ["triton","dispatch","fusion"],visual="tiles")
E("compute-cpu","compute","CPU numerical kernel / BLAS microkernel","Scientific computing · performance","A tightly optimized numerical routine.",
  "Kernel can name a performance-critical computation on any processor. In BLIS, a GEMM microkernel computes a small matrix tile and is embedded in larger blocking loops.",
  "C_{\\rm tile}\\mathrel{+}=A_{\\rm panel}B_{\\rm panel}", "A CPU microkernel keeps a small output tile in registers and uses SIMD instructions to accumulate products.",
  "A BLAS microkernel is a numerical routine, not a small operating-system kernel.", "blas", ["cuda","linux","kpm"],visual="tiles",variants=["GEMM / dot-product kernels","SIMD inner loops","Benchmark computational kernels"])
E("dispatch","compute","Framework operator kernel","PyTorch · tensor runtimes","An implementation selected for an operator and backend.",
  "PyTorch's dispatcher selects registered implementations according to dispatch keys derived from tensors and execution state. Kernels can implement CPU, CUDA, autograd or other behavior.",
  "\\text{operator + dispatch key}\\longmapsto\\text{implementation}", "The same operation may dispatch to a CPU implementation for a CPU tensor and another implementation for a CUDA tensor.",
  "An operator kernel may launch several GPU kernels, call a library, or run entirely on the CPU. It is not necessarily one device launch.", "dispatch", ["cnn","tf","cuda"],visual="layers")
E("tf","compute","TensorFlow OpKernel","TensorFlow internals","The concrete computation implementing an operation.",
  "A TensorFlow custom operation can have a C++ OpKernel class that supplies its Compute method. Registration associates implementations with devices and type constraints.",
  "\\text{operation schema}\\longmapsto\\text{OpKernel implementation}", "A custom CPU operation derives from OpKernel, checks its inputs, allocates an output and computes that output.",
  "The graph operation and its implementation are different layers. An OpKernel need not be a CUDA kernel.", "tf", ["dispatch","cuda"],visual="layers")
E("fusion","compute","Fused / compiler-generated kernel","XLA · optimizing compilers","A routine combining several computations.",
  "A compiler may combine several operations into a generated device kernel, reducing intermediate storage and launch overhead. XLA:GPU describes its fusion operation as compiling to one GPU kernel.",
  "y=\\max(0,a\\cdot x+b)", "A fused pointwise routine can compute multiplication, addition and ReLU while keeping intermediates in registers.",
  "Fusion is a compiler choice with performance constraints. One high-level function or model does not always become one kernel.", "fusion", ["cuda","pallas","dispatch"],visual="tiles")

# Software cores.
E("linux","engine","Operating-system kernel","Operating systems","The core that manages hardware and protected resources.",
  "An OS kernel provides core resource management and privileged mechanisms such as scheduling, memory management and device interaction. Linux is a prominent implementation.",
  "\\text{applications}\\ \\vert\\ \\text{kernel}\\ \\vert\\ \\text{hardware}", "A process requests a file read through a system call; the kernel mediates access and coordinates the relevant system resources.",
  "The Linux kernel is not a whole Linux distribution. Kernel mode is a privilege context, not a second independent meaning of kernel.", "linux", ["microkernel","security","cuda"],visual="layers",variants=["Monolithic (often modular): Linux","Microkernel: seL4","Hybrid: common Windows / XNU classification","Real-time OS kernels"])
E("microkernel","engine","Microkernel","Operating-system architecture","A small privileged OS core with services outside it.",
  "Microkernels retain essential mechanisms such as isolation, scheduling and communication in the core, while many system services live in separate processes.",
  "\\text{services}\\xleftrightarrow{\\rm IPC}\\text{small kernel}", "A filesystem service can execute outside the privileged core and communicate with other components using IPC.",
  "The boundary varies by system. This is an OS architecture, unrelated to a BLAS microkernel.", "sel4", ["linux","compute-cpu","security"],visual="layers",status="Architecture subtype")
E("exokernel","engine","Exokernel","Operating-system research","A protection-focused kernel exposing low-level resources.",
  "An exokernel separates resource protection from higher-level resource management. Library operating systems implement abstractions that conventional kernels often impose.",
  "\\text{protection in kernel; policy in library OS}", "An application-specific library OS can manage its own higher-level storage or memory abstractions while the exokernel enforces resource protection.",
  "An exokernel is not simply a synonym for microkernel; its approach to exposing resources and placing abstractions differs.", "exo", ["linux","microkernel"],visual="layers",status="Architecture subtype")
E("security","engine","Security kernel","Computer security","The mechanisms enforcing the reference monitor.",
  "A security kernel is the trusted computing-base machinery that implements the reference-monitor concept: mediating access, resisting tampering and being amenable to verification.",
  "\\text{subject}\\xrightarrow{\\rm mediated\\ access}\\text{object}", "Every access to a protected object is checked against the system's access rules by the designated trusted mechanism.",
  "The term may include hardware, firmware and software, and need not coincide with the whole OS kernel.", "security", ["linux","lean","microkernel"],visual="layers")
E("lean","engine","Proof-assistant kernel: Lean","Formal methods · type theory","The trusted checker of core proof terms.",
  "Lean's kernel type-checks terms in its core type theory. Elaboration and tactics produce terms that this smaller trusted component checks.",
  "\\Gamma\\vdash p:P", "The term fun h => h proves P→P. A tactic may find this term; the kernel checks that it has the claimed type.",
  "Acceptance is relative to the declared statement and axioms. The kernel does not establish that a formal statement matches an intended informal problem; sorry introduces an assumption.", "lean", ["lcf","security","belief"],visual="proof",variants=["Lean core type checker","Rocq / Coq kernel (related architecture)","Proof terms and declared axioms"])
E("lcf","engine","LCF-style inference kernel","Interactive theorem proving","The small trusted code allowed to construct theorems.",
  "In LCF-style systems, an abstract theorem type can be constructed only through trusted primitive inference operations. Complex proof procedures must reduce their conclusions to those operations.",
  "\\text{primitive inferences}\\longmapsto\\text{theorem value}", "A tactic can be large and experimental, while the operations that certify its result remain in a small inference core.",
  "This architecture is related to, but not identical with, Lean's proof-term type-checking architecture.", "lcf", ["lean"],visual="proof")
E("jupyter","engine","Jupyter / IPython kernel","Interactive computing","The language process that executes notebook code.",
  "A Jupyter kernel runs separately from the user interface, executes code for a language and communicates through the Jupyter messaging protocol.",
  "\\text{notebook UI}\\longleftrightarrow\\text{language process}", "Run x=10 in one Python cell and print(x) in another: the kernel holds the execution state. Restarting it discards that in-memory state.",
  "A notebook's displayed outputs are not its live process state. This kernel is not the OS kernel or a GPU routine.", "jupyter", ["wolfram","linux"],visual="layers",variants=["IPython / ipykernel","IJulia","IRkernel","Other Jupyter language kernels"])
E("wolfram","engine","Wolfram computational kernel","Symbolic computation","The computation engine behind the front end.",
  "Wolfram's notebook front end and computational kernel are separate components. The kernel evaluates Wolfram Language expressions; the front end supplies notebook interaction.",
  "\\text{expression}\\longmapsto\\text{evaluated result}", "A notebook can send an integration expression to the kernel and display the resulting symbolic expression.",
  "A Wolfram kernel process is a computation engine. The word can also appear in mathematical kernel functions evaluated by that same process.", "wolfram", ["jupyter","integral"],visual="layers")
E("cgal","engine","Computational-geometry kernel","Geometry software · CGAL","A package of geometric types, predicates and constructions.",
  "A CGAL kernel supplies geometric primitives and operations: points, lines, orientation tests, intersections and more. Kernels differ in representation and exactness guarantees.",
  "\\text{types + predicates + constructions}", "Exact_predicates_inexact_constructions_kernel gives exact predicate decisions while constructed coordinates may be inexact.",
  "A software geometry kernel and a polygon's visibility kernel are unrelated objects, despite appearing in the same program.", "cgal", ["polygon","cad"],visual="geometry")
E("cad","engine","Geometric modeling / CAD kernel","CAD · engineering software","The engine that builds and modifies geometric models.",
  "A modeling kernel supplies foundational geometry and topology operations for CAD applications, including solid modeling and operations such as Boolean combinations.",
  "\\text{solids}\\longmapsto\\text{Boolean / modeling operations}", "A CAD application uses a modeling kernel to subtract a hole from a solid or update part geometry.",
  "Parasolid and Open CASCADE are examples of this software-engine sense. This is not the visible subset of a polygon.", "cad", ["cgal","polygon"],visual="geometry")
E("simulation","engine","Simulation kernel","SystemC · discrete-event simulation","The central event scheduler and execution machinery.",
  "A simulation kernel coordinates processes, events and simulated time. In SystemC, scheduling and synchronization can include delta cycles that advance computation without advancing physical simulation time.",
  "(t,\\delta)\\longmapsto\\text{scheduled process updates}", "A signal change schedules dependent processes; further same-time updates can run before the simulator advances to the next timed event.",
  "The simulated system's time is different from wall-clock time. A GPU kernel can accelerate a simulation but is not its event scheduler.", "systemc", ["linux","cuda"],visual="timeline")

# Reduced problem instances.
E("kernelization","reduction","Parameterized problem kernel","Algorithms · complexity theory","A reduced equivalent instance bounded by the parameter.",
  "Kernelization is a polynomial-time reduction of (I,k) to an equivalent instance (I′,k′), with total size bounded by a function of k. A polynomial kernel has a polynomial size bound.",
  "(I,k)\\mapsto(I',k'),\\quad |I'|+k'\\le g(k)", "For Vertex Cover with budget k, a vertex of degree greater than k must be chosen. Remove it and reduce k by 1; continue with valid reduction rules.",
  "Equivalent means preserving the answer under the formal definition. Shrinking an input by an arbitrary heuristic is not enough.", "kernelization", ["kernel-search","digraph","belief"],visual="reduce",variants=["Polynomial kernels","Generalized kernels / bikernels","Turing kernelization"])

# Mission data, with a complete useful subtype inventory rather than inflated counts.
E("spice","space","SPICE data kernel","Space science · mission geometry","A data file read by NASA's SPICE toolkit.",
  "SPICE calls its mission-geometry and supporting-data files kernels. They can be binary or text and must be loaded before computations that need their contents.",
  "\\text{loaded kernel files}\\longmapsto\\text{geometry queries}", "Load ephemeris and time-conversion data, then ask SPICE for a body's position at a specified epoch. These kernels contain data; they are not launched as code.",
  "SPICE here means the spacecraft toolkit, not the electronic-circuit simulator. A meta-kernel lists other kernels to load.", "spice spicefiles spk ck pck dsk", ["simulation","cuda"],visual="orbit",variants=[
    ["SPK","Positions and velocities / ephemerides"],
    ["CK","Time-varying orientation / pointing; optional angular rates"],
    ["PCK","Body constants, shapes and orientation models"],
    ["FK","Reference-frame definitions"],
    ["IK","Instrument geometry and parameters"],
    ["LSK","Leapseconds and time-conversion constants"],
    ["SCLK","Spacecraft-clock correlation and conversion"],
    ["DSK","Detailed shape models"],
    ["EK","Event information; less commonly used today"],
    ["MK / meta-kernel","An ordered list of kernel files to load"]
  ])

E("sph","influence","SPH smoothing kernel","Fluid simulation · astrophysics","A spatial weighting function for particle-based fields.",
  "Smoothed particle hydrodynamics approximates continuum fields through a smoothing kernel and particle sums. Smoothing length and kernel shape determine which neighbors contribute and how strongly.",
  "A(r)\\approx\\sum_j\\frac{m_j}{\\rho_j}A_jW(r-r_j,h)", "A compactly supported spline kernel lets a particle gather information from a finite neighborhood rather than from the entire simulation.",
  "The smoothing kernel is a mathematical function. A GPU kernel can execute the particle sum; these are different layers.", "sph", ["mollifier","cuda","convolution"],visual="density",variants=["Cubic spline","Wendland","Gaussian"])
E("attention","similarity","Attention kernel / feature map","Transformer architectures","A pairwise weighting expressed using kernel features.",
  "Kernel formulations of attention express pairwise weights through feature maps. Associativity can then rearrange some attention computations to avoid explicitly forming every pairwise weight.",
  "k(q,k)=\\phi(q)^{\\mathsf T}\\phi(k)", "A nonnegative feature map can give usable attention weights, followed by row normalization and a weighted sum of value vectors.",
  "Distinct query/key projections and row normalization generally do not produce a symmetric PSD token matrix. Not every attention score is a Mercer kernel.", "attention", ["psd","fusion","ntk"],visual="matrix",status="Context-dependent usage")
E("path-kernel","influence","Generating-function kernel","Analytic combinatorics · queueing","The coefficient canceled in the kernel method.",
  "In functional equations for generating functions, a kernel is a coefficient multiplying the unknown function. The kernel method selects a suitable root that cancels this coefficient and exposes a relation among remaining terms.",
  "K(z,u)F(z,u)=R(z,u),\\quad K(z,U(z))=0", "For a walk step polynomial P(u)=u+u⁻¹, a common kernel is 1−zP(u). One chooses a formal root with the required behavior near z=0.",
  "A root cannot be chosen arbitrarily: formal-series and analyticity conditions matter. This kernel method is not machine-learning kernel fitting.", "path", ["transform"],visual="factors",status="Named method")
E("lossy","reduction","Approximate / lossy kernel","Parameterized optimization","A small problem with a controlled approximation loss.",
  "Lossy kernelization relaxes exact preservation for optimization problems. Solutions to the reduced instance are lifted back with a formally bounded degradation in approximation quality.",
  "c\\text{-approximation on }I'\\longmapsto\\alpha c\\text{-approximation on }I", "An α-approximate kernel trades a smaller reduced problem for an explicit factor α in the lifted solution guarantee.",
  "This is still a formal parameterized guarantee, not arbitrary data reduction or an optimization heuristic called Kernel Search.", "lossy", ["kernelization","kernel-search"],visual="reduce",status="Generalization")
