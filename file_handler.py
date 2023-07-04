from os import path
from pandas import DataFrame, read_csv

class FileHandler(object):
    """Procedural class.
    Almacena funcionalidades necesarias para realizar los checks necesarios 
    antes de manipular los files."""
    
    @staticmethod
    def isSpecificFileAndIsNotEmpty(filePath:str) -> bool:
        """Comprueba que el path se trate de un archivo de extensión csv y tenga datos."""
        try:
            return path.isfile(filePath) and filePath.lower().endswith("csv") and path.getsize(filePath) > 0
        except Exception as error:
            return False
    
    @staticmethod
    def keepMandatoryColumns(dataToCheck:DataFrame, mandatoryColumns:list) -> DataFrame:
        """Para confirmar que el DataFrame pueda ser visualizado, necesita contener ciertas columnas.
        En nuestro caso (tenemos las columna hardcoded en la propia QTableView), truncaremos las columnas
        para mantener sólo las mandatory"""
        if set(mandatoryColumns).issubset(set(dataToCheck.columns)):
            return dataToCheck[mandatoryColumns]
        return DataFrame()
        
    @staticmethod
    def readCSV(filePath:str, mandatoryColumns:list) -> DataFrame:
        """Realiza basic checks antes de retornar el DataFrame si cumple con los stándares.
        - Es un archivo csv
        - Contiene datos
        - Contiene ciertas columnas
        
        :param filePath: el archivo a leer.
        :param mandatoryColumns: las columnas que deberán encontrarse en el archivo.
        :return: el DataFrame leído con las mandatoryColumns (only).
        :raises FileNotFound: el archivo no cumple con los basic checkings.
        :raises ValueError: el DataFrame no contiene las mandatoryColumns."""
        isValid = FileHandler.isSpecificFileAndIsNotEmpty(filePath)
        if not isValid: raise FileNotFoundError(f"{filePath} no es un archivo válido o está vacío.")
        readData = read_csv(filePath).fillna("")
        readData = FileHandler.keepMandatoryColumns(readData, mandatoryColumns)
        if readData.empty: raise ValueError(f"{filePath} no contiene las columnas necesarias para ser cargado.")
        return readData
    
    @staticmethod
    def createCSVIfNotExisting(filePath:str, lineToWrite:str) -> str:
        """Crea el archivo en caso de no existir.
        Simplemente crea el archivo con las mandatory columns."""
        if not FileHandler.isSpecificFileAndIsNotEmpty(filePath):
            with open(filePath, "w+") as file:
                file.write(lineToWrite)
        return filePath
    