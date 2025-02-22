# if you don't have PyPDF2: conda install -c conda-forge pypdf2
from PyPDF2 import PdfFileReader, PdfFileWriter  
from os import replace
import tempfile


def add_pdf_metadata(pdf_file, metadata_dict):
    """
    Adds a Python dict to the metadata in a pdf_file.
    Uses PyPDF2 and a temporary file.
    This is an alternative to using PdfPages from matplotlib.backends.backend_pdf 
    PyPDF2 needs the keys in the dict to have a "/" in front;  these are added
     automagically by this function. Furthermore the keys can't have whitespace and
     the values must be strings.
    
    Parameters
    ----------
    pdf_file : str
        The pdf file to be modified.
    metadata_dict : dict
        dict to be added to the pdf metadata (without "/" in front of names,
          no spaces in names, and only strings for values).
    """
    
    assert isinstance(metadata_dict, dict), \
                      "2nd argument must be a dict"
    
    # Initialize the Reader object with the pdf file passed to the function
    fin = open(pdf_file, 'rb')  # 'rb' is read, binary
    reader = PdfFileReader(fin)  
    
    # Copy to the Writer object the pages from the input pdf file
    writer = PdfFileWriter()
    writer.appendPagesFromReader(reader)          
        
    # Copy over the existing metadata    
    metadata = reader.getDocumentInfo()
    writer.addMetadata(metadata)
    
    # Append the custom metadata dict with user entries, prefixing "/" to keys
    metadata_dict_added = {}
    for key, value in metadata_dict.items():
        new_key = "/" + key
        metadata_dict_added[new_key] = value
    writer.addMetadata(metadata_dict_added)
    
    # Write out the full pdf file to a temporary file
    _, temp_file_path = tempfile.mkstemp()
    fout = open(temp_file_path, 'wb')  # 'wb' is write, binary
    writer.write(fout)
    
    # Close up the input and output streams 
    fin.close()
    fout.close()
    
    # Move the temporary file to the original file
    replace(temp_file_path, pdf_file)


def get_pdf_metadata(pdf_file, exclude=True):
    """
    Get the metadata from a pdf as a dict, stripping the leading "/"s.
    Uses PyPDF2.
    
    Parameters
    ----------
    pdf_file : str
        The pdf file to get the metadata from.
    exclude : bool, optional
        Only return the custom metadata. Default: True.
    """

    fin = open(pdf_file, 'rb')
    reader = PdfFileReader(fin)
    metadata = reader.getDocumentInfo()  # gets *all* of the metadata
    
    # Close up the input stream 
    fin.close()
    
    # Standard pdf keys according to Adobe.  Removed if exclude=True
    if exclude:
        pdf_keys = ["/Producer", "/CreationDate", "/Creator", "/Author",
                    "/Subject", "/Title", "/Keywords", "/ModDate"]
        for key in pdf_keys:
            if key in metadata:
                del metadata[key]

    # Remove leading "/"s and convert from PyPDF2 object to a simple dict
    stripped_metadata = {}
    for key, value in metadata.items():
        new_key = key.replace("/", "", 1)  # only replace if at front of string
        stripped_metadata[new_key] = value
                
    return stripped_metadata
