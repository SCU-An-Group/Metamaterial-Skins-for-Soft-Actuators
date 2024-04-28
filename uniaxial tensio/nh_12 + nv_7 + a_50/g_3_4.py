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
mdb.models['Model-1'].materials['pdms'].Density(table=((1.2E-09, ), ))
#meterials3
mdb.models['Model-1'].Material(name='hard ecoflex')
mdb.models['Model-1'].materials['hard ecoflex'].Hyperelastic(materialType=
    ISOTROPIC, table=((1.0, 0.02), ), testData=OFF, type=NEO_HOOKE, 
    volumetricResponse=VOLUMETRIC_DATA)



mdb.openAcis('F:/abaqus tube/express/N_g_3_1.SAT', scaleFromFile=ON)
mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
    THREE_D, geometryFile=mdb.acis, name='N_g_3', type=DEFORMABLE_BODY)
mdb.models['Model-1'].PartFromGeometryFile(bodyNum=2, combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='P_g_3', type=
    DEFORMABLE_BODY)



mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='P_g_3', part=
    mdb.models['Model-1'].parts['P_g_3'])



# creat set
mdb.models['Model-1'].parts['N_g_3'].Set(cells=
    mdb.models['Model-1'].parts['N_g_3'].cells, name='Set-N')
mdb.models['Model-1'].parts['P_g_3'].Set(cells=
    mdb.models['Model-1'].parts['P_g_3'].cells, name='Set-P')





# creat section
mdb.models['Model-1'].HomogeneousSolidSection(material='pdms', name=
    'Section-ex', thickness=None)
# SectionAssignment
mdb.models['Model-1'].parts['P_g_3'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['P_g_3'].sets['Set-P'], sectionName=
    'Section-ex', thicknessAssignment=FROM_SECTION)



# step
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].ImplicitDynamicsStep(alpha=DEFAULT, amplitude=RAMP, 
    application=QUASI_STATIC, initialConditions=OFF, initialInc=1e-10, maxInc=
    0.005, maxNumInc=10000, minInc=1e-10, name='Step-1', nlgeom=ON, nohaf=OFF, 
    previous='Initial', timePeriod=1.0)

# RP
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-3', type=
    DEFORMABLE_BODY)
RP_1 = mdb.models['Model-1'].parts['Part-3'].ReferencePoint(point=(0.0, 0.0, 0.0))
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-3-1', 
    part=mdb.models['Model-1'].parts['Part-3'])
mdb.models['Model-1'].parts['Part-3'].Set(name='Set-1', referencePoints=(
    mdb.models['Model-1'].parts['Part-3'].referencePoints[RP_1.id], ))




# equation
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['P_g_3'].faces.findAt(((
    51.705379, 100.575, 0.666667), ), ((59.821161, 100.575, 0.666667), ), ((
    67.936943, 100.575, 0.666667), ), ((76.052722, 100.575, 0.666667), ), ((
    84.168503, 100.575, 0.666667), ), ((92.284286, 100.575, 0.666667), ), ), 
    name='Set-t')
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['P_g_3'].faces.findAt(((
    51.705379, -3.725, 1.333333), ), ((59.821161, -3.725, 1.333333), ), ((
    67.936943, -3.725, 1.333333), ), ((76.052722, -3.725, 1.333333), ), ((
    84.168503, -3.725, 1.333333), ), ((92.284286, -3.725, 1.333333), ), ), 
    name='Set-bc')
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].Equation(name='Constraint-1', terms=((1.0, 'Set-t', 1), (
    -1.0, 'Part-3-1.Set-1', 1)))




# BC
mdb.models['Model-1'].XsymmBC(createStepName='Step-1', localCsys=None, name=
    'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-bc'])
mdb.models['Model-1'].ZsymmBC(createStepName='Step-1', localCsys=None, name=
    'BC-2', region=mdb.models['Model-1'].rootAssembly.sets['Set-bc'])



# displacement
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-3', region=
    mdb.models['Model-1'].rootAssembly.instances['Part-3-1'].sets['Set-1'], u1=
    UNSET, u2=20.0, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)



# mesh
mdb.models['Model-1'].parts['P_g_3'].setMeshControls(elemShape=TET, regions=
    mdb.models['Model-1'].parts['P_g_3'].cells, technique=FREE)
mdb.models['Model-1'].parts['P_g_3'].setElementType(elemTypes=(ElemType(
    elemCode=C3D10H, elemLibrary=STANDARD), ElemType(elemCode=C3D10H, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D10H, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['P_g_3'].cells, ))
mdb.models['Model-1'].parts['P_g_3'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=1.0)
mdb.models['Model-1'].parts['P_g_3'].generateMesh()





# point
mdb.models['Model-1'].rootAssembly.Set(name='Set-y', vertices=
    mdb.models['Model-1'].rootAssembly.instances['P_g_3'].vertices.findAt(((
    75.529123, 100.575, 2.0), )))
mdb.models['Model-1'].rootAssembly.Set(name='Set-x', vertices=
    mdb.models['Model-1'].rootAssembly.instances['P_g_3'].vertices.findAt(((
    96.603974, 52.15, 2.0), )))


# ODB output
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 
    'COORD'))


mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-2', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-y'], sectionPoints=DEFAULT, 
    variables=('COOR1', 'COOR2', 'COOR3'))
mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-3', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['Set-x'], sectionPoints=DEFAULT, 
    variables=('COOR1', 'COOR2', 'COOR3'))



mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(timeInterval=
    0.01)
mdb.models['Model-1'].historyOutputRequests['H-Output-2'].setValues(
    timeInterval=0.01)
mdb.models['Model-1'].historyOutputRequests['H-Output-3'].setValues(
    timeInterval=0.01)



Parameters = '_alpha_' +  "%g"%alpha
# # Job
jobName = 'g_3_4-MU37' +Parameters
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









stepName = 'Step-1'
outputSetName = 'SET-X'#Rember to CAPSLOCK if rename set

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


os.chdir(main_dir)

curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '//ResultFiles_x'):
    os.makedirs('ResultFiles_x')
os.chdir('ResultFiles_x')

for fm in range(0, len(odb.steps[stepName].frames)):
    outfile = open('X-Y-Z-' + jobName +'x' + Parameters + '_' + str(fm) + '.csv','w')
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
outputSetName = 'SET-Y'#Rember to CAPSLOCK if rename set

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os

os.chdir(main_dir)

curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '//ResultFiles_y'):
    os.makedirs('ResultFiles_y')
os.chdir('ResultFiles_y')


for fm in range(0, len(odb.steps[stepName].frames)):
    outfile = open('X-Y-Z-' + jobName +'y' + Parameters + '_' + str(fm) + '.csv','w')
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