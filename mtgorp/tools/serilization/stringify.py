import typing as t

from mtgorp.models.persistent.printing import Printing


class PrintingLister(object):
	
	@staticmethod
	def something(printings: t.Iterable[Printing]):
		pass