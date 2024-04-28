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

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE) 

Mdb()
#Material ecoflex for Tube
# mu = 0.05 # MPa
mu = 0.037
K1 = 50.0*mu
# MPa ~ 0.49 Poisson ratio
C10 = mu/2.0
D1 = 2.0/K1


#Material pdms for Exoskeleton
alpha = 50.0
mu1 = alpha*mu
vvv = 50.0
K1_1 = vvv*mu1
# MPa ~ 0.49 Poisson ratio  #2.5

C10_1 = mu1/2.0
D1_1 = 2.0/K1_1



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
    ISOTROPIC, table=((1.0, 0.02), ), testData=OFF, type=NEO_HOOKE, 
    volumetricResponse=VOLUMETRIC_DATA)




mdb.openAcis('F:/abaqus tube/display-odb/D.SAT', scaleFromFile=ON)
mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
    THREE_D, geometryFile=mdb.acis, name='D1', type=DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=2, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='D2-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=3, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='D2-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=4, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='D3-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=5, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='D3-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=6, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='D5', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=7, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='D4-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=8, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='D4-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=9, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='tube', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=10, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='cover', type=
    DEFORMABLE_BODY)




# creat set
mdb.models['Model-1'].parts['D2-1'].Set(cells=
    mdb.models['Model-1'].parts['D2-1'].cells, name='Set-D2-1')
mdb.models['Model-1'].parts['D2-2'].Set(cells=
    mdb.models['Model-1'].parts['D2-2'].cells, name='Set-D2-2')
mdb.models['Model-1'].parts['D1'].Set(cells=
    mdb.models['Model-1'].parts['D1'].cells, name='Set-D1')
mdb.models['Model-1'].parts['D3-1'].Set(cells=
    mdb.models['Model-1'].parts['D3-1'].cells, name='Set-D3-1')
mdb.models['Model-1'].parts['D3-2'].Set(cells=
    mdb.models['Model-1'].parts['D3-2'].cells, name='Set-D3-2')
mdb.models['Model-1'].parts['D4-1'].Set(cells=
    mdb.models['Model-1'].parts['D4-1'].cells, name='Set-D4-1')
mdb.models['Model-1'].parts['D4-2'].Set(cells=
    mdb.models['Model-1'].parts['D4-2'].cells, name='Set-D4-2')
mdb.models['Model-1'].parts['D5'].Set(cells=
    mdb.models['Model-1'].parts['D5'].cells, name='Set-D5')


mdb.models['Model-1'].parts['tube'].Set(cells=
    mdb.models['Model-1'].parts['tube'].cells, name='Set-tube')
mdb.models['Model-1'].parts['cover'].Set(cells=
    mdb.models['Model-1'].parts['cover'].cells, name='Set-cover')



mdb.models['Model-1'].parts['D2-2'].PartitionCellByPlaneThreePoints(cells=
    mdb.models['Model-1'].parts['D2-2'].cells.findAt(((7.84974, 128.112641, 
    17.638788), )), point1=mdb.models['Model-1'].parts['D2-2'].vertices.findAt(
    (23.561945, 128.875, 31.0), ), point2=
    mdb.models['Model-1'].parts['D2-2'].vertices.findAt((23.561945, 128.875, 
    33.0), ), point3=mdb.models['Model-1'].parts['D2-2'].vertices.findAt((
    23.561945, 116.975, 33.0), ))
mdb.models['Model-1'].parts['D2-2'].Set(cells=
    mdb.models['Model-1'].parts['D2-2'].cells.findAt(((11.139848, 118.43764, 
    26.188227), )), name='Set-D2-2-1')
mdb.models['Model-1'].parts['D2-2'].Set(cells=
    mdb.models['Model-1'].parts['D2-2'].cells.findAt(((39.196306, 80.487359, 
    18.433136), )), name='Set-D2-2-2')
mdb.models['Model-1'].parts['D4-1'].PartitionCellByPlaneThreePoints(cells=
    mdb.models['Model-1'].parts['D4-1'].cells.findAt(((24.36389, 196.925003, 
    32.313011), )), point1=mdb.models['Model-1'].parts['D4-1'].vertices.findAt(
    (38.061945, 248.075, 16.5), ), point2=
    mdb.models['Model-1'].parts['D4-1'].vertices.findAt((40.061945, 248.075, 
    16.5), ), point3=mdb.models['Model-1'].parts['D4-1'].vertices.findAt((
    40.061945, 236.175, 16.5), ))
mdb.models['Model-1'].parts['D4-1'].Set(cells=
    mdb.models['Model-1'].parts['D4-1'].cells.findAt(((29.504996, 195.20621, 
    30.37406), )), name='Set-D4-1-1')
mdb.models['Model-1'].parts['D4-1'].Set(cells=
    mdb.models['Model-1'].parts['D4-1'].cells.findAt(((29.170015, 231.66879, 
    2.487186), )), name='Set-D4-1-2')



mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='D1-1', part=
    mdb.models['Model-1'].parts['D1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='D2-1-1', part=
    mdb.models['Model-1'].parts['D2-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='D2-2-1', part=
    mdb.models['Model-1'].parts['D2-2'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='D3-1-1', part=
    mdb.models['Model-1'].parts['D3-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='D3-2-1', part=
    mdb.models['Model-1'].parts['D3-2'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='D4-1-1', part=
    mdb.models['Model-1'].parts['D4-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='D4-2-1', part=
    mdb.models['Model-1'].parts['D4-2'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='D5-1', part=
    mdb.models['Model-1'].parts['D5'])
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=(mdb.models['Model-1'].rootAssembly.instances['D1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['D2-1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['D2-2-1'], 
    mdb.models['Model-1'].rootAssembly.instances['D3-1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['D3-2-1'], 
    mdb.models['Model-1'].rootAssembly.instances['D4-1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['D4-2-1'], 
    mdb.models['Model-1'].rootAssembly.instances['D5-1']), keepIntersections=ON
    , name='ex', originalInstances=SUPPRESS)



# creat set
mdb.models['Model-1'].parts['ex'].Set(cells=
    mdb.models['Model-1'].parts['ex'].cells, name='Set-ex')
mdb.models['Model-1'].parts['tube'].Set(cells=
    mdb.models['Model-1'].parts['tube'].cells, name='Set-tube')
mdb.models['Model-1'].parts['cover'].Set(cells=
    mdb.models['Model-1'].parts['cover'].cells, name='Set-cover')



# creat section
mdb.models['Model-1'].HomogeneousSolidSection(material='pdms', name=
    'Section-ex', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='ecoflex', name=
    'Section-tube', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='hard ecoflex', name=
    'Section-cover', thickness=None)
# SectionAssignment
mdb.models['Model-1'].parts['ex'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['ex'].sets['Set-ex'], sectionName=
    'Section-ex', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['tube'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['tube'].sets['Set-tube'], sectionName=
    'Section-tube', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['cover'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['cover'].sets['Set-cover'], sectionName=
    'Section-cover', thicknessAssignment=FROM_SECTION)



# assembly
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='tube-1', 
    part=mdb.models['Model-1'].parts['tube'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='cover-1', 
    part=mdb.models['Model-1'].parts['cover'])
# merge
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=(mdb.models['Model-1'].rootAssembly.instances['tube-1'], 
    mdb.models['Model-1'].rootAssembly.instances['cover-1']), 
    keepIntersections=ON, name='Part-tube', originalInstances=SUPPRESS)



# step
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].ImplicitDynamicsStep(alpha=DEFAULT, amplitude=RAMP, 
    application=QUASI_STATIC, initialConditions=OFF, initialInc=1e-10, maxInc=
    0.005, maxNumInc=10000, minInc=1e-10, name='Step-1', nlgeom=ON, nohaf=OFF, 
    previous='Initial', timePeriod=1.0)





# # contact interaction
# # surface
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-ex', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['ex-1'].faces.findAt(((
    10.420887, 253.299998, 10.371166), ), ((9.117038, 283.100006, 17.762803), 
    ), ((18.603554, 230.950002, 2.874129), ), ((38.059877, 201.891663, 
    16.255126), ), ((38.006851, 201.149999, 17.762803), ), ((9.936074, 
    171.350001, 21.458391), ), ((37.567869, 187.991669, 12.747124), ), ((
    17.433111, 73.758334, 29.641058), ), ((24.824748, 119.199999, 30.944907), 
    ), ((37.567869, 128.391668, 12.747124), ), ((9.49464, 12.416667, 
    12.984189), ), ((9.064013, 64.566668, 16.744874), ), ))
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-tube', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].faces.findAt(((
    25.443686, 193.608329, 2.12262), ), ((21.680203, 193.608329, 30.87738), ), 
    ))




# tie_3
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-ex'], name='Constraint-1'
    , positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-tube'], thickness=ON, 
    tieRotations=ON)


# # BC
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].faces.findAt(((
    11.213427, -3.725, 19.917683), ), )+\
    mdb.models['Model-1'].rootAssembly.instances['ex-1'].faces.findAt(((
    9.082134, -3.725, 11.993797), ), ((13.275163, -3.725, 5.357608), ), ((
    20.224525, -3.725, 1.707014), ), ((28.251545, -3.725, 1.379245), ), ((
    35.183634, -3.725, 5.749842), ), ((38.041756, -3.725, 11.993797), ), ((
    39.001705, -3.725, 19.999065), ), ((33.848727, -3.725, 27.642392), ), ((
    26.899364, -3.725, 31.292985), ), ((18.872345, -3.725, 31.620756), ), ((
    11.940254, -3.725, 27.250158), ), ((8.122186, -3.725, 19.999065), ), ), 
    name='Set-1')
mdb.models['Model-1'].EncastreBC(createStepName='Initial', localCsys=None, 
    name='BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-1'])




# fluid cavity
# referencePoints
RP_1 = mdb.models['Model-1'].rootAssembly.ReferencePoint(point=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].InterestingPoint(
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].edges.findAt((
    23.561945, -1.725, 4.0), ), CENTER))
mdb.models['Model-1'].rootAssembly.Set(name='Set-RP', referencePoints=(
    mdb.models['Model-1'].rootAssembly.referencePoints[RP_1.id], ))
# cavity surfaces
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-cavity', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].faces.findAt(((
    12.91667, 292.275, 19.446278), ), ((21.939754, 194.274996, 4.105707), ), ((
    25.184136, 194.274996, 28.894293), ), ((12.91667, -1.725, 13.553722), ), ))
# fluid property
mdb.models['Model-1'].FluidCavityProperty(expansionTable=((1.0, ), ), 
    fluidDensity=1.29e-12, name='IntProp-2', useExpansion=True)
mdb.models['Model-1'].FluidCavity(cavityPoint=
    mdb.models['Model-1'].rootAssembly.sets['Set-RP'], cavitySurface=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-cavity'], createStepName=
    'Initial', interactionProperty='IntProp-2', name='Int-2')
# volume control
mdb.models['Model-1'].Temperature(createStepName='Initial', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(0.0, ), name='Predefined Field-1', region=
    mdb.models['Model-1'].rootAssembly.sets['Set-RP'])
mdb.models['Model-1'].predefinedFields['Predefined Field-1'].setValuesInStep(
    magnitudes=(3.0, ), stepName='Step-1')





mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 
    'COORD'))




# history output
mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-2', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-RP'], sectionPoints=DEFAULT, 
    variables=('PCAV', 'CVOL'))






# mesh
mdb.models['Model-1'].parts['ex'].setMeshControls(elemShape=TET, regions=
    mdb.models['Model-1'].parts['ex'].cells, technique=FREE)
mdb.models['Model-1'].parts['ex'].setElementType(elemTypes=(ElemType(
    elemCode=C3D10H, elemLibrary=STANDARD), ElemType(elemCode=C3D10H, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D10H, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['ex'].cells, ))
mdb.models['Model-1'].parts['ex'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=1.0)
mdb.models['Model-1'].parts['ex'].generateMesh()

mdb.models['Model-1'].parts['Part-tube'].setMeshControls(elemShape=TET, 
    regions=mdb.models['Model-1'].parts['Part-tube'].cells, technique=
    FREE)
mdb.models['Model-1'].parts['Part-tube'].setElementType(elemTypes=(ElemType(
    elemCode=C3D10H, elemLibrary=STANDARD), ElemType(elemCode=C3D10H, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D10H, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['Part-tube'].cells, ))
mdb.models['Model-1'].parts['Part-tube'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=1.0)
mdb.models['Model-1'].parts['Part-tube'].generateMesh()





mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(timeInterval=
    0.01)
mdb.models['Model-1'].historyOutputRequests['H-Output-2'].setValues(
    timeInterval=0.01)

















Parameters = '_alpha_' +  "%g"%alpha
# # Job
jobName = 'D-MU37' +Parameters
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




# job
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name=jobName, nodalOutputPrecision=SINGLE, 
    numCpus=64, numDomains=64, numGPUs=0, queue=None, resultsFormat=ODB, 
    scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()



