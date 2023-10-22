package com.bccard.gallery.backend.controller;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.bccard.gallery.backend.entity.Item;
import com.bccard.gallery.backend.repository.ItemRepository;

@RestController
public class CrawlingController {
	
    /**
     * 조회할 URL셋팅 및 Document 객체 로드하기
     */
    private static final String url = "https://kr.iherb.com/pr/california-gold-nutrition-pterostilbene-50-mg-180-veggie-capsules/101513";
    
    @GetMapping("/api/prdDetail")
    public String crawl() {
        Connection conn = Jsoup.connect(url)
        		.userAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71")
        		.referrer("https://kr.iherb.com/")
        		.header("sec-ch-ua", "\".Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"103\", \"Chromium\";v=\"103\"");
        
        Document document = null;
        try {            
            //url의 내용을 HTML Document 객체로 가져온다.
            //https://jsoup.org/apidocs/org/jsoup/nodes/Document.html 참고
        	document = conn.get();
        } catch (IOException e) {
            e.printStackTrace();
        }

//        List<String> list = getDataList(document);
        return this.getSelectorValue(document);
    }

    /**
     * css selector data 가져오기
     */
    private String getSelectorValue(Document document) {
        
        Elements selects = document.select("#stock-status > div.text-danger.stock-status-text");//select 메서드 안에 css selector를 작성하여 Elements를 가져올 수 있다.
        System.out.println(selects.html());
        return selects.html();
    }

    /**
     * data가져오기
     */
    private List<String> getDataList(Document document) {
        List<String> list = new ArrayList<>();
        Elements selects = document.select("#stock-status > div.text-danger.stock-status-text");//select 메서드 안에 css selector를 작성하여 Elements를 가져올 수 있다.

        for (Element select : selects) {
            System.out.println(select.html());
            //html(), text(), children(), append().... 등 다양한 메서드 사용 가능
            //https://jsoup.org/apidocs/org/jsoup/nodes/Element.html 참고
        }
        return list;
    }


}



