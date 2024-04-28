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




mdb.openAcis('E:/abaqus cube/display/U43.SAT', scaleFromFile=ON)
mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
    THREE_D, geometryFile=mdb.acis, name='g3-1', type=DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=2, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='g3-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=3, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='g23-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=4, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='g23-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=5, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='g33-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=6, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='g33-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=7, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='g7-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=8, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='g7-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=9, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='g27-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=10, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='g27-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=11, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='tube', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=12, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='cover', type=
    DEFORMABLE_BODY)




# creat set
mdb.models['Model-1'].parts['g3-1'].Set(cells=
    mdb.models['Model-1'].parts['g3-1'].cells, name='Set-g3-1')
mdb.models['Model-1'].parts['g3-2'].Set(cells=
    mdb.models['Model-1'].parts['g3-2'].cells, name='Set-g3-2')
mdb.models['Model-1'].parts['g7-1'].Set(cells=
    mdb.models['Model-1'].parts['g7-1'].cells, name='Set-g7-1')
mdb.models['Model-1'].parts['g7-2'].Set(cells=
    mdb.models['Model-1'].parts['g7-2'].cells, name='Set-g7-2')

mdb.models['Model-1'].parts['g23-1'].Set(cells=
    mdb.models['Model-1'].parts['g23-1'].cells, name='Set-g23-1')
mdb.models['Model-1'].parts['g23-2'].Set(cells=
    mdb.models['Model-1'].parts['g23-2'].cells, name='Set-g23-2')

mdb.models['Model-1'].parts['g27-1'].Set(cells=
    mdb.models['Model-1'].parts['g27-1'].cells, name='Set-g27-1')
mdb.models['Model-1'].parts['g27-2'].Set(cells=
    mdb.models['Model-1'].parts['g27-2'].cells, name='Set-g27-2')
mdb.models['Model-1'].parts['g33-1'].Set(cells=
    mdb.models['Model-1'].parts['g33-1'].cells, name='Set-g33-1')
mdb.models['Model-1'].parts['g33-2'].Set(cells=
    mdb.models['Model-1'].parts['g33-2'].cells, name='Set-g33-2')

mdb.models['Model-1'].parts['tube'].Set(cells=
    mdb.models['Model-1'].parts['tube'].cells, name='Set-tube')
mdb.models['Model-1'].parts['cover'].Set(cells=
    mdb.models['Model-1'].parts['cover'].cells, name='Set-cover')



mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g3-1-1', part=
    mdb.models['Model-1'].parts['g3-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g3-2-1', part=
    mdb.models['Model-1'].parts['g3-2'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g23-1-1', part=
    mdb.models['Model-1'].parts['g23-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g23-2-1', part=
    mdb.models['Model-1'].parts['g23-2'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g7-1-1', part=
    mdb.models['Model-1'].parts['g7-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g7-2-1', part=
    mdb.models['Model-1'].parts['g7-2'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g33-1-1', part=
    mdb.models['Model-1'].parts['g33-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g33-2-1', part=
    mdb.models['Model-1'].parts['g33-2'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g27-1-1', part=
    mdb.models['Model-1'].parts['g27-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='g27-2-1', part=
    mdb.models['Model-1'].parts['g27-2'])
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=(mdb.models['Model-1'].rootAssembly.instances['g3-1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['g3-2-1'], 
    mdb.models['Model-1'].rootAssembly.instances['g23-1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['g23-2-1'], 
    mdb.models['Model-1'].rootAssembly.instances['g7-1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['g7-2-1'],  
    mdb.models['Model-1'].rootAssembly.instances['g33-1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['g33-2-1'], 
    mdb.models['Model-1'].rootAssembly.instances['g27-1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['g27-2-1']), 
    keepIntersections=ON, name='ex', originalInstances=SUPPRESS)



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
    8.299528, 418.700012, -15.31604), ), ((8.282289, 418.700012, -14.09198), ), 
    ((8.781241, -4.95, -18.292282), ), ((8.278615, -13.383334, -14.255126), ), 
    ((8.299528, -117.699997, -15.31604), ), ((8.282289, -117.699997, 
    -14.09198), ), ((8.781241, 322.850006, -18.292282), ), ((8.278615, 
    314.416677, -14.255126), ), ((36.771853, -3.95, -18.292282), ), ((
    37.243468, 210.933334, -13.521132), ), ))
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-tube', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].faces.findAt(((
    24.658288, 212.749995, -28.87738), ), ((20.894805, 212.749995, -0.12262), 
    ), ))




# tie_3
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-ex'], name='Constraint-1'
    , positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-tube'], thickness=ON, 
    tieRotations=ON)


# # BC
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].faces.findAt(((
    10.428029, -213.05, -11.082317), ), )+\
    mdb.models['Model-1'].rootAssembly.instances['ex-1'].faces.findAt(((
    7.498257, -213.05, -18.647707), ), ((11.430916, -213.05, -25.541117), ), ((
    18.214809, -213.05, -29.659821), ), ((25.98892, -213.05, -29.320643), ), ((
    32.777761, -213.05, -25.899408), ), ((37.05323, -213.05, -19.613426), ), ((
    37.05323, -213.05, -9.386575), ), ((32.777761, -213.05, -3.100592), ), ((
    25.98892, -213.05, 0.320643), ), ((18.214809, -213.05, 0.65982), ), ((
    11.430916, -213.05, -3.458883), ), ((7.498257, -213.05, -10.352294), ), ), 
    name='Set-BC')
mdb.models['Model-1'].EncastreBC(createStepName='Initial', localCsys=None, 
    name='BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-BC'])



# fluid cavity
# referencePoints
RP_1 = mdb.models['Model-1'].rootAssembly.ReferencePoint(point=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].InterestingPoint(
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].edges.findAt((
    22.776547, -211.05, -27.0), ), CENTER))
mdb.models['Model-1'].rootAssembly.Set(name='Set-RP', referencePoints=(
    mdb.models['Model-1'].rootAssembly.referencePoints[RP_1.id], ))
# cavity surfaces
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-cavity', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].faces.findAt(((
    12.131272, 425.65, -11.553722), ), ((21.154356, 213.416662, -26.894293), ), 
    ((24.398737, 213.416662, -2.105707), ), ((12.131272, -211.05, -17.446278), 
    ), ))
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






# # mesh
# mdb.models['Model-1'].parts['ex'].setMeshControls(elemShape=TET, regions=
#     mdb.models['Model-1'].parts['ex'].cells, technique=FREE)
# mdb.models['Model-1'].parts['ex'].setElementType(elemTypes=(ElemType(
#     elemCode=C3D10H, elemLibrary=STANDARD), ElemType(elemCode=C3D10H, 
#     elemLibrary=STANDARD), ElemType(elemCode=C3D10H, elemLibrary=STANDARD)), 
#     regions=(mdb.models['Model-1'].parts['ex'].cells, ))
# mdb.models['Model-1'].parts['ex'].seedPart(deviationFactor=0.1, 
#     minSizeFactor=0.1, size=1.0)
# mdb.models['Model-1'].parts['ex'].generateMesh()

# mdb.models['Model-1'].parts['Part-tube'].setMeshControls(elemShape=TET, 
#     regions=mdb.models['Model-1'].parts['Part-tube'].cells, technique=
#     FREE)
# mdb.models['Model-1'].parts['Part-tube'].setElementType(elemTypes=(ElemType(
#     elemCode=C3D10H, elemLibrary=STANDARD), ElemType(elemCode=C3D10H, 
#     elemLibrary=STANDARD), ElemType(elemCode=C3D10H, elemLibrary=STANDARD)), 
#     regions=(mdb.models['Model-1'].parts['Part-tube'].cells, ))
# mdb.models['Model-1'].parts['Part-tube'].seedPart(deviationFactor=0.1, 
#     minSizeFactor=0.1, size=35.0)
# mdb.models['Model-1'].parts['Part-tube'].generateMesh()





# mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(timeInterval=
#     0.01)
# mdb.models['Model-1'].historyOutputRequests['H-Output-2'].setValues(
#     timeInterval=0.01)

















Parameters = '_alpha_' +  "%g"%alpha
# # Job
jobName = 'U43-2-MU37' +Parameters
###############################################
###   Create new directionary for FE files  ###
###############################################

# DirName = jobName
# curr_dir = os.getcwd()
# if not os.path.exists(curr_dir + '//FEModelFiles'):
#     os.mkdir(curr_dir + '//FEModelFiles')
# if not os.path.exists(curr_dir + '//FEModelFiles//' + DirName):
#     os.mkdir(curr_dir + '//FEModelFiles//' + DirName)
# os.chdir(curr_dir + '//FEModelFiles//' + DirName)




# job
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name=jobName, nodalOutputPrecision=SINGLE, 
    numCpus=64, numDomains=64, numGPUs=0, queue=None, resultsFormat=ODB, 
    scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.saveAs(pathName=jobName)
# mdb.jobs[jobName].submit()
# mdb.jobs[jobName].waitForCompletion()



