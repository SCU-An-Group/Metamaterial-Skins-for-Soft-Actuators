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



# import part
mdb.openStep('E:/abaqus cube/3D/cg/G5ex.STEP', scaleFromFile=ON)
mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
    THREE_D, geometryFile=mdb.acis, name='G5ex', type=DEFORMABLE_BODY)
mdb.openStep('E:/abaqus cube/3D/cg/G5tube.STEP', scaleFromFile=
    ON)
mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
    THREE_D, geometryFile=mdb.acis, name='G5tube-1', type=DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=2, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='G5tube-2', type=
    DEFORMABLE_BODY)

# # import part
# mdb.openStep('E:/CAE DirectoryName/last/FEModelFiles/G5/G5ex.STEP', scaleFromFile=ON)
# mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
#     THREE_D, geometryFile=mdb.acis, name='G5ex', type=DEFORMABLE_BODY)
# mdb.openStep('E:/CAE DirectoryName/last/FEModelFiles/G5/G5tube.STEP', scaleFromFile=
#     ON)
# mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
#     THREE_D, geometryFile=mdb.acis, name='G5tube-1', type=DEFORMABLE_BODY)
# mdb.models['Model-1'].PartFromGeometryFile(bodyNum=2, combine=False, 
#     dimensionality=THREE_D, geometryFile=mdb.acis, name='G5tube-2', type=
#     DEFORMABLE_BODY)


# creat set
mdb.models['Model-1'].parts['G5ex'].Set(cells=
    mdb.models['Model-1'].parts['G5ex'].cells, name='Set-ex')
mdb.models['Model-1'].parts['G5tube-2'].Set(cells=
    mdb.models['Model-1'].parts['G5tube-2'].cells, name='Set-tube')
mdb.models['Model-1'].parts['G5tube-1'].Set(cells=
    mdb.models['Model-1'].parts['G5tube-1'].cells, name='Set-cover')



# creat section
mdb.models['Model-1'].HomogeneousSolidSection(material='pdms', name=
    'Section-ex', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='ecoflex', name=
    'Section-tube', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='hard ecoflex', name=
    'Section-cover', thickness=None)
# SectionAssignment
mdb.models['Model-1'].parts['G5ex'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['G5ex'].sets['Set-ex'], sectionName=
    'Section-ex', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['G5tube-2'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['G5tube-2'].sets['Set-tube'], sectionName=
    'Section-tube', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['G5tube-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['G5tube-1'].sets['Set-cover'], sectionName=
    'Section-cover', thicknessAssignment=FROM_SECTION)



# assembly
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='G5ex-1', 
    part=mdb.models['Model-1'].parts['G5ex'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='G5tube-1-1', 
    part=mdb.models['Model-1'].parts['G5tube-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='G5tube-2-1', 
    part=mdb.models['Model-1'].parts['G5tube-2'])
# merge
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=(mdb.models['Model-1'].rootAssembly.instances['G5tube-1-1'], 
    mdb.models['Model-1'].rootAssembly.instances['G5tube-2-1']), 
    keepIntersections=ON, name='Part-tube', originalInstances=SUPPRESS)



# step
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].ImplicitDynamicsStep(alpha=DEFAULT, amplitude=RAMP, 
    application=QUASI_STATIC, initialConditions=OFF, initialInc=1e-13, maxInc=
    0.005, maxNumInc=10000, minInc=1e-15, name='Step-1', nlgeom=ON, nohaf=OFF, 
    previous='Initial', timePeriod=1.0)



# contact interaction
# surface
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-ex', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['G5ex-1'].faces.findAt(((
    14.369519, 100.572202, 51.999055), ), ((14.47086, 95.188649, 53.70715), ), 
    ))
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-tube', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].faces.findAt(((
    30.379615, 70.472203, 37.574677), ), ((27.359422, 70.472203, 66.41698), ), 
    ))



# tie_3
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-ex'], name='Constraint-1'
    , positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-tube'], thickness=ON, 
    tieRotations=ON)


# BC
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['G5ex-1'].faces.findAt(((
    14.230602, 2.272201, 48.036926), ), ((17.991295, 2.272201, 41.430082), ), (
    (24.485758, 2.272201, 37.47848), ), ((32.23807, 2.272201, 36.52707), ), ((
    39.321818, 2.272201, 40.105536), ), ((43.778834, 2.272201, 46.672114), ), (
    (43.146203, 2.272201, 57.109253), ), ((38.870733, 2.272201, 63.395236), ), 
    ((33.431257, 2.272201, 67.15565), ), ((25.657146, 2.272201, 66.816472), ), 
    ((18.868305, 2.272201, 63.395236), ), ((14.592836, 2.272201, 57.109253), ), 
    )+mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].faces.findAt(
    ((28.869519, 2.272201, 66.022708), ), ), name='Set-BC')
mdb.models['Model-1'].EncastreBC(createStepName='Initial', localCsys=None, 
    name='BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-BC'])



# fluid cavity
# RFpoint
RP_1 = mdb.models['Model-1'].rootAssembly.ReferencePoint(point=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].vertices.findAt(
    (28.869519, 4.272201, 39.495829), ))
mdb.models['Model-1'].rootAssembly.Set(name='Set-RP', referencePoints=(
    mdb.models['Model-1'].rootAssembly.referencePoints[RP_1.id], ))
# cavitySurface
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-cavity', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].faces.findAt(((
    27.424943, 71.13887, 39.579581), ), ((30.314094, 71.13887, 64.412076), ), (
    (28.869519, 4.272201, 39.998391), ), ((17.054348, 104.572201, 54.079163), 
    ), ))
# fluid property
mdb.models['Model-1'].FluidCavityProperty(bulkModulusTable=((2000.0, ), ), 
    expansionTable=((1.0, ), ), fluidDensity=1e-09, name='IntProp-2', 
    useBulkModulus=True, useExpansion=True)
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



# history output
mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-2', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-RP'], sectionPoints=DEFAULT, 
    variables=('PCAV', 'CVOL'))

#create testline
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].edges.findAt(
    ((28.869519, 78.997201, 66.495829), )), name='Set-testline_in')

mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].edges.findAt(
    ((28.869519, 78.997201,37.495829), )), name='Set-testline_out')

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


# mesh
mdb.models['Model-1'].parts['G5ex'].setMeshControls(elemShape=TET, regions=
    mdb.models['Model-1'].parts['G5ex'].cells.findAt(((14.784355, 12.594872, 
    57.435606), )), technique=FREE)
mdb.models['Model-1'].parts['G5ex'].setElementType(elemTypes=(ElemType(
    elemCode=C3D10H, elemLibrary=STANDARD), ElemType(elemCode=C3D10H, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D10H, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['G5ex'].cells.findAt(((14.784355, 
    12.594872, 57.435606), )), ))
mdb.models['Model-1'].parts['G5ex'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=1.0)
mdb.models['Model-1'].parts['G5ex'].generateMesh()
mdb.models['Model-1'].parts['G5ex'].setElementType(elemTypes=(ElemType(
    elemCode=C3D10H, elemLibrary=STANDARD), ElemType(elemCode=C3D10H, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D10H, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, distortionControl=DEFAULT)), regions=(
    mdb.models['Model-1'].parts['G5ex'].cells.findAt(((14.784355, 12.594872, 
    57.435606), )), ))

mdb.models['Model-1'].parts['Part-tube'].setMeshControls(elemShape=TET, 
    regions=mdb.models['Model-1'].parts['Part-tube'].cells.findAt(((28.869519, 
    106.572201, 37.707068), ), ((28.869519, 2.272201, 66.022708), ), ), 
    technique=FREE)
mdb.models['Model-1'].parts['Part-tube'].setElementType(elemTypes=(ElemType(
    elemCode=C3D10H, elemLibrary=STANDARD), ElemType(elemCode=C3D10H, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D10H, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['Part-tube'].cells.findAt(((28.869519, 
    106.572201, 37.707068), ), ((28.869519, 2.272201, 66.022708), ), ), ))
mdb.models['Model-1'].parts['Part-tube'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=1.0)
mdb.models['Model-1'].parts['Part-tube'].generateMesh()
mdb.models['Model-1'].parts['Part-tube'].setElementType(elemTypes=(ElemType(
    elemCode=C3D10H, elemLibrary=STANDARD), ElemType(elemCode=C3D10H, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D10H, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, distortionControl=DEFAULT)), regions=(
    mdb.models['Model-1'].parts['Part-tube'].cells.findAt(((28.869519, 
    2.272201, 66.022708), )), ))


mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(timeInterval=
    0.01)
mdb.models['Model-1'].historyOutputRequests['H-Output-2'].setValues(
    timeInterval=0.01)







mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].rootAssembly.Set(name='Set-PI', nodes=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].nodes[408:409])
mdb.models['Model-1'].rootAssembly.Set(name='Set-PO', nodes=
    mdb.models['Model-1'].rootAssembly.instances['Part-tube-1'].nodes[509:510])


mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-5', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-PI'], sectionPoints=DEFAULT, 
    variables=('COOR1', 'COOR2', 'COOR3'))
mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-6', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-PO'], sectionPoints=DEFAULT, 
    variables=('COOR1', 'COOR2', 'COOR3'))







Parameters = '_alpha_' +  "%g"%alpha
# # Job
jobName ='G5_mu0037_point' +Parameters

##############################################
##   Create new directionary for FE files  ###
##############################################

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



# stepName = 'Step-1'
# outputSetName = 'SET-TESTLINE_IN'
# # Rember to CAPSLOCK if renamed set

# from odbAccess import*
# from abaqusConstants import*
# import string
# import numpy as np
# import os

# odb = openOdb(path = jobName+'.odb')

# curr_dir = os.getcwd()
# if not os.path.exists(curr_dir + '//ResultFiles'):
#     os.makedirs('ResultFiles')
# os.chdir('ResultFiles')

# main_dir = os.getcwd()

# curr_dir = os.getcwd()
# if not os.path.exists(curr_dir + '//ResultFiles_LI'):
#     os.makedirs('ResultFiles_LI')
# os.chdir('ResultFiles_LI')

# for fm in range(0, len(odb.steps[stepName].frames)):
#     outfile = open('X-Z-' + jobName +'LI' + Parameters + '_' + str(fm) + '.csv','w')
#     timeFrame = odb.steps[stepName].frames[fm]
#     readNode = odb.rootAssembly.nodeSets[outputSetName]
#     Coordinate = timeFrame.fieldOutputs['COORD']
#     readNodeCoordinate = Coordinate.getSubset(region=readNode)
#     readNodeCoordinateValues = readNodeCoordinate.values
#     count=len(readNodeCoordinateValues)
#     Y_Coordinate = np.zeros(count)
#     Z_Coordinate = np.zeros(count)
#     for i in range(0, count):
#         Y_Coordinate[i]=readNodeCoordinateValues[i].data[1]
#         Z_Coordinate[i]=readNodeCoordinateValues[i].data[2]
#     Sorted_Z_Coordinate = np.sort(Z_Coordinate)
#     Inps = Z_Coordinate.argsort()
#     Sorted_Y_Coordinate = Y_Coordinate[Inps]
#     for i in range(0, count):
#         outfile.write(str(Sorted_Y_Coordinate[i]) + ',' +
#         str(Sorted_Z_Coordinate[i]) + ','  + '\n')
#     outfile.close()

# stepName = 'Step-1'
# outputSetName = 'SET-TESTLINE_OUT'
# # Rember to CAPSLOCK if renamed set

# from odbAccess import*
# from abaqusConstants import*
# import string
# import numpy as np
# import os

# os.chdir(main_dir)

# curr_dir = os.getcwd()
# if not os.path.exists(curr_dir + '//ResultFiles_LO'):
#     os.makedirs('ResultFiles_LO')
# os.chdir('ResultFiles_LO')

# for fm in range(0, len(odb.steps[stepName].frames)):
#     outfile = open('X-Z-' + jobName +'LO' + Parameters + '_' + str(fm) + '.csv','w')
#     timeFrame = odb.steps[stepName].frames[fm]
#     readNode = odb.rootAssembly.nodeSets[outputSetName]
#     Coordinate = timeFrame.fieldOutputs['COORD']
#     readNodeCoordinate = Coordinate.getSubset(region=readNode)
#     readNodeCoordinateValues = readNodeCoordinate.values
#     count=len(readNodeCoordinateValues)
#     Y_Coordinate = np.zeros(count)
#     Z_Coordinate = np.zeros(count)
#     for i in range(0, count):
#         Y_Coordinate[i]=readNodeCoordinateValues[i].data[1]
#         Z_Coordinate[i]=readNodeCoordinateValues[i].data[2]
#     Sorted_Z_Coordinate = np.sort(Z_Coordinate)
#     Inps = Z_Coordinate.argsort()
#     Sorted_Y_Coordinate = Y_Coordinate[Inps]
#     for i in range(0, count):
#         outfile.write(str(Sorted_Y_Coordinate[i]) + ',' +
#         str(Sorted_Z_Coordinate[i]) + ','  + '\n')
#     outfile.close()


# from odbAccess import*
# from abaqusConstants import*
# import string
# import numpy as np
# import os


# region = 'Node ASSEMBLY.1'
# fileName = '/P-V-'

# os.chdir(main_dir)
# curr_dir = os.getcwd()
# if not os.path.exists(curr_dir + '//ResultFiles_PV'):
#     os.makedirs('ResultFiles_PV')
# os.chdir('ResultFiles_PV')
# curr_dir = os.getcwd()

# data = []
# curr_dir = os.getcwd()
# volumeValues = np.array(odb.steps[stepName].historyRegions[region].historyOutputs['CVOL'].data)
# pressureValues = np.array(odb.steps[stepName].historyRegions[region].historyOutputs['PCAV'].data)

# for i in range(len(volumeValues)):
#     data.append([odb.steps[stepName].historyRegions[region].historyOutputs['CVOL'].data[i][1], odb.steps[stepName].historyRegions[region].historyOutputs['PCAV'].data[i][1]])
# data = np.array(data)
# np.savetxt(curr_dir + fileName + jobName + Parameters + '.csv',data, delimiter =  ',', fmt = '%.10e',header = 'Volume, Pressure')


# odb.close()