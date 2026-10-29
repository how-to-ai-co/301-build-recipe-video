import Vision; import AppKit; import CoreImage
let a=CommandLine.arguments; let img=CIImage(contentsOf:URL(fileURLWithPath:a[1]))!
let h=VNImageRequestHandler(ciImage:img); let r=VNGenerateForegroundInstanceMaskRequest(); try! h.perform([r])
let o=r.results!.first!; let buf=try! o.generateMaskedImage(ofInstances:o.allInstances,from:h,croppedToInstancesExtent:true)
let ci=CIImage(cvPixelBuffer:buf); let ctx=CIContext()
try! ctx.writePNGRepresentation(of:ci,to:URL(fileURLWithPath:a[2]),format:.RGBA8,colorSpace:CGColorSpaceCreateDeviceRGB())
