package com.bccard.gallery.backend.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.bccard.gallery.backend.entity.Item;
import com.bccard.gallery.backend.repository.ItemRepository;

@RestController
public class ItemController {
	
	@Autowired
    ItemRepository itemRepository;

    @GetMapping("/api/crawling")
    public List<Item> getItems() {
        List<Item> items = itemRepository.findAll();
        return items;
    }

}

