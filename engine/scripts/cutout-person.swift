// Person-only background removal (VNGeneratePersonSegmentationRequest, accurate). Usage: cutout-person in.jpg out.png
import Vision; import CoreImage; import AppKit
let a = CommandLine.arguments; let img = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!.oriented(.up)
let r = VNGeneratePersonSegmentationRequest(); r.qualityLevel = .accurate; r.outputPixelFormat = kCVPixelFormatType_OneComponent8
try! VNImageRequestHandler(ciImage: img).perform([r])
var mask = CIImage(cvPixelBuffer: r.results!.first!.pixelBuffer)
mask = mask.transformed(by: CGAffineTransform(scaleX: img.extent.width / mask.extent.width, y: img.extent.height / mask.extent.height))
let clear = CIImage(color: .clear).cropped(to: img.extent)
let out = img.applyingFilter("CIBlendWithMask", parameters: [kCIInputBackgroundImageKey: clear, kCIInputMaskImageKey: mask])
try! CIContext().writePNGRepresentation(of: out, to: URL(fileURLWithPath: a[2]), format: .RGBA8, colorSpace: CGColorSpaceCreateDeviceRGB())
