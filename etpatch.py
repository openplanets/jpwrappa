#
# Copyright 2012 The SCAPE Project Consortium
#
# This software is copyrighted by the SCAPE Project Consortium.
# The SCAPE project is co-funded by the European Union under
# FP7 ICT-2009.4.1 (Grant Agreement number 270137).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# etpatch.py by Rene van der Ark, KB / National Library of the Netherlands

import xml.etree.ElementTree as ET
#from byteconv import bytesToText

# TODO:
# 1) Find out whether these patches are necessary
# 2) learn how to write and test patches properly


# I don't want to mess with ANYthing :)
def tostring(elem, enc, meth):
	return ET.tostring(elem, enc, meth)
def fromstring(text):
	return ET.fromstring(text)
def SubElement(parent, tag):
	return ET.SubElement(parent, tag)

class Element(ET.Element):
	
	# Replacement for ET's 'findtext' function, which has a bug
	# that will return empty string if text field contains integer with
	# value of zero (0); If there is no match, return None
	def findElementText(self, match):
		elt = self.find(match)
		if elt is not None:
			return(elt.text)
		else:
			return(None)


	def findAllText(self, match):
		# Searches element and returns list that contains 'Text' attribute
		# of all matching sub-elements. Returns empty list if element
		# does not exist
	
		try:
			return [result.text for result in self.findall(match)]
		except:
			return []

	
	def appendChildTagWithText(self, tag, text):
		# Append childnode with text
		
		el = ET.SubElement(self, tag)
		el.text = text
		
	def appendIfNotEmpty(self,subelement):
		# Append sub-element, but only if subelement is not empty
		
		if len(subelement) != 0:
			self.append(subelement)
	
	def makeHumanReadable(self, remapTable = {}):
		# Takes element object, and returns a modified version in which all
		# non-printable 'text' fields (which may contain numeric data or binary strings)
		# are replaced by printable strings
		#
		# Property values in original tree may be mapped to alternative (more user-friendly)
		# reportable values using a remapTable, which is a nested dictionary.

		for elt in self.iter():
			# Text field of this element
			textIn = elt.text
			
			# Tag name
			tag = elt.tag
			
			# Step 1: replace property values by values defined in enumerationsMap,
			# if applicable
			try:
				# If tag is in enumerationsMap, replace property values
				parameterMap = remapTable[tag]
				try:
					# Map original property values to values in dictionary
					remappedValue = parameterMap[textIn]
				except KeyError:
					# If value doesn't match any key: use original value instead
					remappedValue = textIn
			except KeyError:
				# If tag doesn't match any key in enumerationsMap, use original value
				remappedValue = textIn
			
			# Step 2: convert all values to text strings
			if remappedValue != None:
				# Data type
				textType = type(remappedValue)
		
				# Convert text field, depending on type
				if textType == bytes:
					textOut = bytesToText(remappedValue)
				elif textType in[int,float,bool]:
					textOut=str(remappedValue)
				else:
					textOut=remappedValue
	
				# Update output tree
				elt.text = textOut
			


	def toxml(self, indent = "  "):
		return(ET.tostring(self, 'ascii','xml'))
		
		# Disabled pretty-printing for now as minidom appears to choke on
		# entity references, i.e. code below will go wrong:
		#
		# return minidom.parseString(selfAsString).toprettyxml(indent)
	
	def totext(self, indent = "  "):
		return(ET.tostring(self, 'ascii','text'))

