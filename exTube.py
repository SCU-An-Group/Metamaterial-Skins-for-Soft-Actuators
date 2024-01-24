# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

execfile("Parameters_for_exTube.py")
# -*- coding: UTF-8 -*- 
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE) 

Mdb()
float_n_hoop = float(n_hoop)
float_n_vertical = float(n_vertical)

h = 14.9
K = h*float_n_vertical/R

# Length = 120.0
# h = Length/n_vertical


Length = K*R
Cg = g/h 

theta = 2.0*pi/n_hoop

# w = 14.0
# R = w/(2.0*sin(pi/float_n_hoop))
w = 2.0*R*sin(pi/float_n_hoop)

D = R*cos(pi/float_n_hoop)


#About Proportion of structure
n_hoop_negative = n_hoop/2
n_hoop_positive = n_hoop/2
# n_hoop_negative = n_hoop/(Beta+1)
# n_hoop_positive = n_hoop-n_hoop_negative


#About material
#Neo-Hookean shear modulus mu; bulk modulus K1

#Material ecoflex for Tube
# mu = 0.05 # MPa

K1 = 50.0*mu
# MPa ~ 0.49 Poisson ratio

C10 = mu/2.0
D1 = 2.0/K1


#Material pdms for Exoskeleton
mu1 = alpha*mu
K1_1 = vvv*mu1
# MPa ~ 0.49 Poisson ratio  #2.5

C10_1 = mu1/2.0
D1_1 = 2.0/K1_1
#0.8


#creat meterials
#meterials1
mdb.models['Model-1'].Material(name='ecoflex')
mdb.models['Model-1'].materials['ecoflex'].Hyperelastic(materialType=ISOTROPIC, 
    table=((C10, D1), ),testData=OFF, type=NEO_HOOKE, volumetricResponse=
    VOLUMETRIC_DATA)

#meterials2
mdb.models['Model-1'].Material(name='pdms')
mdb.models['Model-1'].materials['pdms'].Hyperelastic(materialType=ISOTROPIC, 
    table=((C10_1, D1_1), ), testData=OFF, type=NEO_HOOKE, volumetricResponse=
    VOLUMETRIC_DATA)

#meterials3
mdb.models['Model-1'].Material(name='hard ecoflex')
mdb.models['Model-1'].materials['hard ecoflex'].Hyperelastic(materialType=
    ISOTROPIC, table=((1.0, 0.8), ), testData=OFF, type=NEO_HOOKE, 
    volumetricResponse=VOLUMETRIC_DATA)
#######################################################################################################
#################################     create exoskeleton     ##########################################
#######################################################################################################

#creat part positive
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)

mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, 0.0), point2=(0.0, (h-g)/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, (h-g)/2.0), point2=(-w/2.0, g/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(-w/2.0, g/2.0), point2=(-w/2.0, h-g/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(-w/2.0, h-g/2.0), point2=(0.0, (h-g)/2.0 + g))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, (h-g)/2.0 + g), point2=(w/2.0, h-g/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(w/2.0, h-g/2.0), point2=(w/2.0, g/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(w/2.0, g/2.0), point2=(0.0, (h-g)/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, (h+g)/2.0), point2=(0.0, h))

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Positive', type=
    DEFORMABLE_BODY)

mdb.models['Model-1'].parts['Positive'].BaseWire(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

#creat part negative
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)

mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, 0.0), point2=(0.0, g/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, g/2.0), point2=(-w/2.0, (h-g)/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(-w/2.0, (h-g)/2.0), point2=(-w/2.0, (h+g)/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(-w/2.0, (h+g)/2.0), point2=(0.0, h-g/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, h-g/2.0), point2=(w/2.0, (h+g)/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(w/2.0, (h+g)/2.0), point2=(w/2.0, (h-g)/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(w/2.0, (h-g)/2.0), point2=(0.0, g/2.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, h-g/2.0), point2=(0.0, h))

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Negative', type=
    DEFORMABLE_BODY)

mdb.models['Model-1'].parts['Negative'].BaseWire(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

#Create axis
datum_1 = mdb.models['Model-1'].rootAssembly.DatumPointByCoordinate(coords=(0.0, 0.0, D))
datum_2 = mdb.models['Model-1'].rootAssembly.DatumPointByCoordinate(coords=(0.0, 1.0, D))
axis_1 = mdb.models['Model-1'].rootAssembly.DatumAxisByTwoPoint(point1=
    mdb.models['Model-1'].rootAssembly.datums[datum_1.id], point2=
    mdb.models['Model-1'].rootAssembly.datums[datum_2.id])



#####################################################################################################
# Assembly instances positive-1-1 and creat Part-P
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Positive-1', 
    part=mdb.models['Model-1'].parts['Positive'])

mdb.models['Model-1'].rootAssembly.LinearInstancePattern(
    direction1=(1.0, 0.0, 0.0), direction2=(0.0, 1.0, 0.0), 
    instanceList=('Positive-1', ), 
    number1=1, number2=n_vertical, 
    spacing1=6.0, spacing2=h)

SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()

mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0), 
    instanceList=(SingleInstances_List), number=n_hoop_positive, point=(0.0, 0.5, 
    D), totalAngle=180.0 - theta*180.0/pi)

SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()

mdb.models['Model-1'].rootAssembly.rotate(
    angle=theta*180.0/pi/2.0, 
    axisDirection=(0.0, 10.0, 0.0), 
    axisPoint=(0.0, 0.5, D), 
    instanceList=(SingleInstances_List))


SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()

mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=([mdb.models['Model-1'].rootAssembly.instances[SingleInstances_List[i]]
    for i in range(len(SingleInstances_List))]), 
    name='Part-P', originalInstances=SUPPRESS)

root_assembly = mdb.models['Model-1'].rootAssembly
SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()
for instance_name in SingleInstances_List:
    del root_assembly.instances[instance_name]

#####################################################################################################
#Assembly instances negative-1-1 and creat Part-N
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Negative-1', 
    part=mdb.models['Model-1'].parts['Negative'])

mdb.models['Model-1'].rootAssembly.LinearInstancePattern(
    direction1=(-1.0, 0.0, 0.0), direction2=(0.0, 1.0, 0.0), 
    instanceList=('Negative-1', ), 
    number1=1, number2=n_vertical, 
    spacing1=6.0, spacing2=h)

SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()

mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0), 
    instanceList=(SingleInstances_List), number=n_hoop_negative, point=(0.0, 0.5, 
    D), totalAngle=-180.0 + theta*180.0/pi)


SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()

mdb.models['Model-1'].rootAssembly.rotate(
    angle=theta*180.0/pi/2.0, 
    axisDirection=(0.0, 10.0, 0.0), 
    axisPoint=(0.0, 0.5, D), 
    instanceList=(SingleInstances_List))


# theta = 2.0*pi/n_hoop

SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()

mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=([mdb.models['Model-1'].rootAssembly.instances[SingleInstances_List[i]]
    for i in range(len(SingleInstances_List))]), 
    name='Part-N', originalInstances=SUPPRESS)

root_assembly = mdb.models['Model-1'].rootAssembly
SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()
for instance_name in SingleInstances_List:
    del root_assembly.instances[instance_name]
mdb.models['Model-1'].parts['Part-P'].Set(edges=
    mdb.models['Model-1'].parts['Part-P'].edges, name='Set-2')
mdb.models['Model-1'].parts['Part-N'].Set(edges=
    mdb.models['Model-1'].parts['Part-N'].edges, name='Set-1')
#####################################################################################################

#Create Exoskeleton

#Assembly instance negative and positive
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-P-1', 
    part=mdb.models['Model-1'].parts['Part-P'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-N-1', 
    part=mdb.models['Model-1'].parts['Part-N'])
mdb.models['Model-1'].rootAssembly.rotate(angle=-theta*180/pi , axisDirection=(0.0, 
    10.0, 0.0), axisPoint=(0.0, 0.5, D), instanceList=('Part-N-1', ))



#Merge negative and positive to get Exoskeleton
SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()

mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=([mdb.models['Model-1'].rootAssembly.instances[SingleInstances_List[i]]
    for i in range(len(SingleInstances_List))]), 
    name='Exoskeleton', originalInstances=SUPPRESS)

root_assembly = mdb.models['Model-1'].rootAssembly
SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()
for instance_name in SingleInstances_List:
    del root_assembly.instances[instance_name]



#Mesh Exoskeleton
mdb.models['Model-1'].parts['Exoskeleton'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.5)
mdb.models['Model-1'].parts['Exoskeleton'].generateMesh()

#creat section-2
mdb.models['Model-1'].RectangularProfile(a=2.0, b=1.3, name='Profile-1')
mdb.models['Model-1'].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='pdms', name='Section-2', poissonRatio=0.0, 
    profile='Profile-1', temperatureVar=LINEAR)

mdb.models['Model-1'].parts['Exoskeleton'].Set(edges=
    mdb.models['Model-1'].parts['Exoskeleton'].edges, name='Set-4')


#SectionAssignment
mdb.models['Model-1'].parts['Exoskeleton'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=TOP_SURFACE, region=
    mdb.models['Model-1'].parts['Exoskeleton'].sets['Set-4'], sectionName=
    'Section-2', thicknessAssignment=FROM_SECTION)


#Assign Beam Section Direction
mdb.models['Model-1'].parts['Exoskeleton'].assignBeamSectionOrientation(method=
    N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdb.models['Model-1'].parts['Exoskeleton'].sets['Set-4'])

#Assembly Tube and Exoskeleton
datum_3 = mdb.models['Model-1'].rootAssembly.DatumPointByCoordinate(coords=(0.0, 0.0, 0.0))
datum_4 = mdb.models['Model-1'].rootAssembly.DatumPointByCoordinate(coords=(0.0, 0.0, 1.0))
axis_z = mdb.models['Model-1'].rootAssembly.DatumAxisByTwoPoint(point1=
    mdb.models['Model-1'].rootAssembly.datums[datum_3.id], point2=
    mdb.models['Model-1'].rootAssembly.datums[datum_4.id])
axis_2 = mdb.models['Model-1'].rootAssembly.DatumAxisByRotation(angle=90.0, axis=
    mdb.models['Model-1'].rootAssembly.datums[axis_1.id], line=
    mdb.models['Model-1'].rootAssembly.datums[axis_z.id])


#######################################################################################################
########################################     create tube     ##########################################
#######################################################################################################

#create tube
#creat part Tube
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)

for i in range(n_hoop):
    mdb.models['Model-1'].sketches['__profile__'].Line((R*cos(theta/2.0 + i*theta), 
        R*sin(theta/2.0 + i*theta)),
        (R*cos(theta/2.0 + (i + 1)*theta), 
        R*sin(theta/2.0 + (i + 1)*theta)))

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Tube', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Tube'].BaseShellExtrude(depth=Length, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

#creat set:Tube surface 
mdb.models['Model-1'].parts['Tube'].Set(faces=
    mdb.models['Model-1'].parts['Tube'].faces, name='Tube face')

#creat section-tube
mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=SIMPSON, material='ecoflex', name='Section-tube', 
    nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
    preIntegrate=OFF, temperature=GRADIENT, thickness=2.2, thicknessField='', 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
mdb.models['Model-1'].parts['Tube'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Tube'].sets['Tube face'], sectionName=
    'Section-tube', thicknessAssignment=FROM_SECTION)

#creat Part Cover
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)

for i in range(n_hoop):
    mdb.models['Model-1'].sketches['__profile__'].Line((R*cos(theta/2.0 + i*theta), 
        R*sin(theta/2.0 + i*theta)),
        (R*cos(theta/2.0 + (i + 1)*theta), 
        R*sin(theta/2.0 + (i + 1)*theta)))


mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Cover', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Cover'].BaseShell(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

  #creat set:Cover surface 
mdb.models['Model-1'].parts['Cover'].Set(faces=
    mdb.models['Model-1'].parts['Cover'].faces.findAt(((0.0, 0.0, 
    0.0), )), name='Cover face')

#creat section-cover
mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=SIMPSON, material='hard ecoflex', name='Section-cover', 
    nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
    preIntegrate=OFF, temperature=GRADIENT, thickness=2.2, thicknessField='', 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)

mdb.models['Model-1'].parts['Cover'].SectionAssignment(offset=0.0, offsetField=
    '', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Cover'].sets['Cover face'], sectionName=
    'Section-cover', thicknessAssignment=FROM_SECTION)

#creat Instance:Tube + Top +Bottom
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Tube-1', part=
    mdb.models['Model-1'].parts['Tube'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Top', part=
    mdb.models['Model-1'].parts['Cover'])
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Top', ), 
    vector=(0.0, 0.0, Length))
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Bottom', part=
    mdb.models['Model-1'].parts['Cover'])

#merge
SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()

mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=([mdb.models['Model-1'].rootAssembly.instances[SingleInstances_List[i]]
    for i in range(len(SingleInstances_List))]), 
    name='Part-Tube', originalInstances=SUPPRESS)

root_assembly = mdb.models['Model-1'].rootAssembly
SingleInstances_List = mdb.models['Model-1'].rootAssembly.instances.keys()
for instance_name in SingleInstances_List:
    del root_assembly.instances[instance_name]

mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name=
    'Part-Tube-1', part=mdb.models['Model-1'].parts['Part-Tube'])

# creat step
mdb.models['Model-1'].StaticStep(name='Step-1', nlgeom=ON, previous='Initial')
mdb.models['Model-1'].steps['Step-1'].setValues(initialInc=1e-12, maxInc=0.1, 
    maxNumInc=1000, minInc=1e-18)


# creat mesh
mdb.models['Model-1'].parts['Part-Tube'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.5)
mdb.models['Model-1'].parts['Part-Tube'].generateMesh()
mdb.models['Model-1'].parts['Part-Tube'].setElementType(elemTypes=(ElemType(
    elemCode=S4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    hourglassControl=ENHANCED), ElemType(elemCode=S3, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['Part-Tube'].faces, ))


mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-Tube-1'].faces.findAt(((
    0.0, 0.0, 0.0), )), name='Set-BC')
mdb.models['Model-1'].EncastreBC(createStepName='Initial', localCsys=None, name=
    'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-BC'])

#ReferencePoint
datum_RP=mdb.models['Model-1'].rootAssembly.ReferencePoint(point=(D, w/2.0, 0.0))

mdb.models['Model-1'].rootAssembly.Surface(name='Surf-1', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-Tube-1'].faces)
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-2', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-Tube-1'].faces.findAt(((
    0.0, 0.0, Length), )))
mdb.models['Model-1'].rootAssembly.SurfaceByBoolean(name='Surf-CF1', operation=
    DIFFERENCE, surfaces=(
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-1'], 
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-2']))

mdb.models['Model-1'].rootAssembly.Surface(name='Surf-2', side2Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-Tube-1'].faces.findAt(((
    0.0, 0.0, Length), )))
mdb.models['Model-1'].rootAssembly.SurfaceByBoolean(name='Surf-CF', operation=
    UNION, surfaces=(
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-2'], 
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-CF1']))
####################################################################################################
mdb.models['Model-1'].rootAssembly.Set(name='Set-RP', referencePoints=(
    mdb.models['Model-1'].rootAssembly.referencePoints[datum_RP.id], ))

mdb.models['Model-1'].FluidCavityProperty(expansionTable=((1.0, ), ), 
    fluidDensity=1.255e-12, name='IntProp-1', useExpansion=True)

mdb.models['Model-1'].FluidCavity(cavityPoint=
    mdb.models['Model-1'].rootAssembly.sets['Set-RP'], cavitySurface=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-CF'], createStepName=
    'Initial', interactionProperty='IntProp-1', name='Int-1')

mdb.models['Model-1'].Temperature(createStepName='Initial', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(0.0, ), name='Predefined Field-1', region=
    mdb.models['Model-1'].rootAssembly.sets['Set-RP'])
mdb.models['Model-1'].predefinedFields['Predefined Field-1'].setValuesInStep(
    magnitudes=(3, ), stepName='Step-1')

mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-2', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-RP'], sectionPoints=DEFAULT, 
    variables=('PCAV', 'CVOL'))


#######################################################################################################
#######################################################################################################
#Create exoskeleton+tube=extube
#Assembly
if n_vertical % 2 == 0:
    pyc = n_vertical / 2
else:
    pyc = (n_vertical + 1) / 2
if (n_hoop/2) % 2 == 0:   
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Exoskeleton', 
        part=mdb.models['Model-1'].parts['Exoskeleton'])
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(10.0, 0.0, 
        0.0), axisPoint=(0.0, 0.0, D), instanceList=('Exoskeleton', ))
    mdb.models['Model-1'].rootAssembly.rotate(angle=180.0/n_hoop, axisDirection=(0.0, 0.0, 
        10.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Exoskeleton', ))
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Exoskeleton', ), 
        vector=(0.0, 0.0, -D))
else:
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Exoskeleton', 
        part=mdb.models['Model-1'].parts['Exoskeleton'])
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(10.0, 0.0, 
        0.0), axisPoint=(0.0, 0.0, D), instanceList=('Exoskeleton', ))
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Exoskeleton', ), 
        vector=(0.0, 0.0, -D))

#Tie

mdb.models['Model-1'].rootAssembly.Surface(circumEdges=
    mdb.models['Model-1'].rootAssembly.instances['Exoskeleton'].edges, name=
    's_Surf-ex')
mdb.models['Model-1'].rootAssembly.Surface(name='m_Surf-tube', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-Tube-1'].faces)
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.surfaces['m_Surf-tube'], name=
    'Constraint-1', positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.surfaces['s_Surf-ex'], thickness=ON, 
    tieRotations=ON)

#######################################################################################################
########################################     Post Processing     ######################################
#######################################################################################################

#create testline
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-Tube-1'].edges.findAt(
    ((D, w/2, Length-1), )), name='Set-testline_in')

mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-Tube-1'].edges.findAt(
    ((-D, w/2, Length-1), )), name='Set-testline_out')


mdb.models['Model-1'].rootAssembly.Set(name='Set-PI', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Exoskeleton'].vertices.findAt(
    ((D, 0.0,  pyc*h), )))
mdb.models['Model-1'].rootAssembly.Set(name='Set-PO', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Exoskeleton'].vertices.findAt(
    ((-D, 0.0, pyc*h), )))

#create coordinate
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 
    'COORD'))


mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-3', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-testline_in'], sectionPoints=DEFAULT, 
    variables=('COOR1', 'COOR2', 'COOR3'))

mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-4', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-testline_out'], sectionPoints=DEFAULT, 
    variables=('COOR1', 'COOR2', 'COOR3'))

mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-5', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-PI'], sectionPoints=DEFAULT, 
    variables=('COOR1', 'COOR2', 'COOR3'))
mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-6', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-PO'], sectionPoints=DEFAULT, 
    variables=('COOR1', 'COOR2', 'COOR3'))
G = int(g)

MU_str=str(mu).replace(".", "")
MU = int(MU_str)

Parameters = '_G_' +  "%g"%G
# # Job
jobName ='exTubeMU01' +Parameters

###############################################
###   Create new directionary for FE files  ###
###############################################

DirName = jobName
curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '//FEModelFiles'):
    os.mkdir(curr_dir + '//FEModelFiles')
if not os.path.exists(curr_dir + '//FEModelFiles//' + DirName):
    os.mkdir(curr_dir + '//FEModelFiles//' + DirName)
os.chdir(curr_dir + '//FEModelFiles//' + DirName)

mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name=jobName, nodalOutputPrecision=SINGLE, 
    numCpus=64, numDomains=64, numGPUs=0, queue=None, resultsFormat=ODB, 
    scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs[jobName].submit()
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].waitForCompletion()

#############################################################
#     Extract coordinates of nodes in a deformed set       ##
#############################################################

stepName = 'Step-1'
outputSetName = 'SET-TESTLINE_IN'
# Rember to CAPSLOCK if renamed set

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os

odb = openOdb(path = jobName+'.odb')

curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '//ResultFiles'):
    os.makedirs('ResultFiles')
os.chdir('ResultFiles')

main_dir = os.getcwd()

curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '//ResultFiles_LI'):
    os.makedirs('ResultFiles_LI')
os.chdir('ResultFiles_LI')

for fm in range(0, len(odb.steps[stepName].frames)):
    outfile = open('X-Z-' + jobName +'LI' + Parameters + '_' + str(fm) + '.csv','w')
    timeFrame = odb.steps[stepName].frames[fm]
    readNode = odb.rootAssembly.nodeSets[outputSetName]
    Coordinate = timeFrame.fieldOutputs['COORD']
    readNodeCoordinate = Coordinate.getSubset(region=readNode)
    readNodeCoordinateValues = readNodeCoordinate.values
    count=len(readNodeCoordinateValues)
    X_Coordinate = np.zeros(count)
    Z_Coordinate = np.zeros(count)
    for i in range(0, count):
        X_Coordinate[i]=readNodeCoordinateValues[i].data[0]
        Z_Coordinate[i]=readNodeCoordinateValues[i].data[2]
    Sorted_Z_Coordinate = np.sort(Z_Coordinate)
    Inps = Z_Coordinate.argsort()
    Sorted_X_Coordinate = X_Coordinate[Inps]
    for i in range(0, count):
        outfile.write(str(Sorted_X_Coordinate[i]) + ',' +
        str(Sorted_Z_Coordinate[i]) + ','  + '\n')
    outfile.close()

stepName = 'Step-1'
outputSetName = 'SET-TESTLINE_OUT'
# Rember to CAPSLOCK if renamed set

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os

os.chdir(main_dir)

curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '//ResultFiles_LO'):
    os.makedirs('ResultFiles_LO')
os.chdir('ResultFiles_LO')

for fm in range(0, len(odb.steps[stepName].frames)):
    outfile = open('X-Z-' + jobName +'LO' + Parameters + '_' + str(fm) + '.csv','w')
    timeFrame = odb.steps[stepName].frames[fm]
    readNode = odb.rootAssembly.nodeSets[outputSetName]
    Coordinate = timeFrame.fieldOutputs['COORD']
    readNodeCoordinate = Coordinate.getSubset(region=readNode)
    readNodeCoordinateValues = readNodeCoordinate.values
    count=len(readNodeCoordinateValues)
    X_Coordinate = np.zeros(count)
    Z_Coordinate = np.zeros(count)
    for i in range(0, count):
        X_Coordinate[i]=readNodeCoordinateValues[i].data[0]
        Z_Coordinate[i]=readNodeCoordinateValues[i].data[2]
    Sorted_Z_Coordinate = np.sort(Z_Coordinate)
    Inps = Z_Coordinate.argsort()
    Sorted_X_Coordinate = X_Coordinate[Inps]
    for i in range(0, count):
        outfile.write(str(Sorted_X_Coordinate[i]) + ',' +
        str(Sorted_Z_Coordinate[i]) + ','  + '\n')
    outfile.close()



stepName = 'Step-1'
outputSetName = 'SET-PI'#Rember to CAPSLOCK if rename set

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os

os.chdir(main_dir)

curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '//ResultFiles_PI'):
    os.makedirs('ResultFiles_PI')
os.chdir('ResultFiles_PI')

for fm in range(0, len(odb.steps[stepName].frames)):
    outfile = open('X-Y-Z-' + jobName +'PI' + Parameters + '_' + str(fm) + '.csv','w')
    outfile.write('X, Y, Z\n')
    timeFrame = odb.steps[stepName].frames[fm]
    readNode = odb.rootAssembly.nodeSets[outputSetName]
    Coordinate = timeFrame.fieldOutputs['COORD']  # Remember to set field outputs manually
    readNodeCoordinate = Coordinate.getSubset(region=readNode)
    readNodeCoordinateValues = readNodeCoordinate.values
    count=len(readNodeCoordinateValues)
    X_Coordinate = np.zeros(count)
    Y_Coordinate = np.zeros(count)
    Z_Coordinate = np.zeros(count)
    for i in range(0, count):
        X_Coordinate[i]=readNodeCoordinateValues[i].data[0]
        Y_Coordinate[i]=readNodeCoordinateValues[i].data[1]
        Z_Coordinate[i]=readNodeCoordinateValues[i].data[2]
    Sorted_Z_Coordinate = np.sort(Z_Coordinate) # Sort data according to Z coordinates
    Inps = Z_Coordinate.argsort()
    Sorted_X_Coordinate = X_Coordinate[Inps]
    Sorted_Y_Coordinate = Y_Coordinate[Inps]
    for i in range(0, count):
        outfile.write(str(Sorted_X_Coordinate[i]) + ',' +
        str(Sorted_Y_Coordinate[i]) + ','  +
        str(Sorted_Z_Coordinate[i]) + ','  + '\n')
    outfile.close()

stepName = 'Step-1'
outputSetName = 'SET-PO'#Rember to CAPSLOCK if rename set

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os

os.chdir(main_dir)

curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '//ResultFiles_PO'):
    os.makedirs('ResultFiles_PO')
os.chdir('ResultFiles_PO')


for fm in range(0, len(odb.steps[stepName].frames)):
    outfile = open('X-Y-Z-' + jobName +'PO' + Parameters + '_' + str(fm) + '.csv','w')
    outfile.write('X, Y, Z\n')
    timeFrame = odb.steps[stepName].frames[fm]
    readNode = odb.rootAssembly.nodeSets[outputSetName]
    Coordinate = timeFrame.fieldOutputs['COORD']  # Remember to set field outputs manually
    readNodeCoordinate = Coordinate.getSubset(region=readNode)
    readNodeCoordinateValues = readNodeCoordinate.values
    count=len(readNodeCoordinateValues)
    X_Coordinate = np.zeros(count)
    Y_Coordinate = np.zeros(count)
    Z_Coordinate = np.zeros(count)
    for i in range(0, count):
        X_Coordinate[i]=readNodeCoordinateValues[i].data[0]
        Y_Coordinate[i]=readNodeCoordinateValues[i].data[1]
        Z_Coordinate[i]=readNodeCoordinateValues[i].data[2]
    Sorted_Z_Coordinate = np.sort(Z_Coordinate) # Sort data according to Z coordinates
    Inps = Z_Coordinate.argsort()
    Sorted_X_Coordinate = X_Coordinate[Inps]
    Sorted_Y_Coordinate = Y_Coordinate[Inps]
    for i in range(0, count):
        outfile.write(str(Sorted_X_Coordinate[i]) + ',' +
        str(Sorted_Y_Coordinate[i]) + ','  +
        str(Sorted_Z_Coordinate[i]) + ','  + '\n')
    outfile.close()



from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os


region = 'Node ASSEMBLY.1'
fileName = '/P-V-'

os.chdir(main_dir)
curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '//ResultFiles_PV'):
    os.makedirs('ResultFiles_PV')
os.chdir('ResultFiles_PV')
curr_dir = os.getcwd()

data = []
curr_dir = os.getcwd()
volumeValues = np.array(odb.steps[stepName].historyRegions[region].historyOutputs['CVOL'].data)
pressureValues = np.array(odb.steps[stepName].historyRegions[region].historyOutputs['PCAV'].data)

for i in range(len(volumeValues)):
    data.append([odb.steps[stepName].historyRegions[region].historyOutputs['CVOL'].data[i][1], odb.steps[stepName].historyRegions[region].historyOutputs['PCAV'].data[i][1]])
data = np.array(data)
np.savetxt(curr_dir + fileName + jobName + Parameters + '.csv',data, delimiter =  ',', fmt = '%.10e',header = 'Volume, Pressure')


odb.close()

